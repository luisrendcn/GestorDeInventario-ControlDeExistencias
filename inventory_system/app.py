"""
app.py
======
Aplicación Flask para Control de Existencias con BD SQLite.

Interfaz web para gestionar inventario.
"""

import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

from db import db as database
from models.producto import Producto

# Cargar variables de entorno
load_dotenv()

# Crear aplicación Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
CORS(app)

# Inicializar BD
@app.before_request
def init_db():
    """Inicializa conexión a la BD antes de cada request"""
    try:
        if not database.conn:
            database.conectar()
    except Exception as e:
        print(f"⚠️ Error al inicializar BD: {e}")
        # No lanzar error aquí, permitir que Flask maneje
        pass


# Manejo global de errores
@app.errorhandler(404)
def not_found(error):
    """Error 404 - No encontrado"""
    return jsonify({"error": "Recurso no encontrado"}), 404


@app.errorhandler(500)
def internal_error(error):
    """Error 500 - Error interno del servidor"""
    return jsonify({"error": "Error interno del servidor"}), 500


# ============================================================================
# RUTAS - PÁGINA PRINCIPAL
# ============================================================================

@app.route('/')
def index():
    """Página principal."""
    return render_template('index.html')


# ============================================================================
# API - PRODUCTOS
# ============================================================================

@app.route('/api/productos', methods=['GET'])
def listar_productos():
    """Lista todos los productos."""
    try:
        productos = database.listar_productos()
        return jsonify(productos)
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/api/productos/<producto_id>', methods=['GET'])
def obtener_producto(producto_id):
    """Obtiene un producto específico."""
    try:
        producto = database.obtener_producto(producto_id)
        if not producto:
            return jsonify({"error": "Producto no encontrado"}), 404
        return jsonify(producto)
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/api/productos', methods=['POST'])
def crear_producto():
    """Crea un nuevo producto."""
    try:
        datos = request.get_json()
        
        # Validar datos
        campos_requeridos = ['id', 'nombre', 'precio', 'stock']
        for campo in campos_requeridos:
            if campo not in datos:
                return jsonify({"error": f"Falta campo: {campo}"}), 400
        
        # Crear producto
        producto = Producto(
            id=datos['id'],
            nombre=datos['nombre'],
            precio=float(datos['precio']),
            stock=int(datos['stock']),
            stock_minimo=int(datos.get('stock_minimo', 5)),
            descripcion=datos.get('descripcion')
        )
        
        database.crear_producto(producto)
        # Obtener el producto creado desde la BD como dict
        producto_db = database.obtener_producto(producto.id)
        return jsonify(producto_db), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/productos/<producto_id>', methods=['DELETE'])
def eliminar_producto(producto_id):
    """Elimina un producto."""
    try:
        if database.eliminar_producto(producto_id):
            return jsonify({"mensaje": "Producto eliminado"}), 200
        return jsonify({"error": "Producto no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ============================================================================
# API - OPERACIONES DE STOCK
# ============================================================================

@app.route('/api/entrada', methods=['POST'])
def registrar_entrada():
    """Registra una entrada de stock."""
    try:
        datos = request.get_json()
        
        # Validar datos
        if 'producto_id' not in datos or 'cantidad' not in datos:
            return jsonify({"error": "Faltan datos requeridos"}), 400
        
        producto_id = datos['producto_id']
        cantidad = int(datos['cantidad'])
        motivo = datos.get('motivo', 'Entrada')
        
        if cantidad <= 0:
            return jsonify({"error": "Cantidad debe ser positiva"}), 400
        
        # Obtener producto actual
        producto = database.obtener_producto(producto_id)
        if not producto:
            return jsonify({"error": "Producto no encontrado"}), 404
        
        # Actualizar stock
        nuevo_stock = producto['stock'] + cantidad
        database.actualizar_stock(
            producto_id=producto_id,
            nuevo_stock=nuevo_stock,
            tipo='entrada',
            cantidad=cantidad,
            motivo=motivo
        )
        
        # Retornar producto actualizado
        producto_actualizado = database.obtener_producto(producto_id)
        return jsonify({
            "mensaje": f"Entrada de {cantidad} unidades registrada",
            "producto": producto_actualizado
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/salida', methods=['POST'])
def registrar_salida():
    """Registra una salida de stock."""
    try:
        datos = request.get_json()
        
        # Validar datos
        if 'producto_id' not in datos or 'cantidad' not in datos:
            return jsonify({"error": "Faltan datos requeridos"}), 400
        
        producto_id = datos['producto_id']
        cantidad = int(datos['cantidad'])
        motivo = datos.get('motivo', 'Salida')
        
        if cantidad <= 0:
            return jsonify({"error": "Cantidad debe ser positiva"}), 400
        
        # Obtener producto actual
        producto = database.obtener_producto(producto_id)
        if not producto:
            return jsonify({"error": "Producto no encontrado"}), 404
        
        # Validar stock suficiente
        if cantidad > producto['stock']:
            return jsonify({
                "error": f"Stock insuficiente. Disponible: {producto['stock']}, solicitado: {cantidad}"
            }), 400
        
        # Actualizar stock
        nuevo_stock = producto['stock'] - cantidad
        database.actualizar_stock(
            producto_id=producto_id,
            nuevo_stock=nuevo_stock,
            tipo='salida',
            cantidad=cantidad,
            motivo=motivo
        )
        
        # Retornar producto actualizado
        producto_actualizado = database.obtener_producto(producto_id)
        return jsonify({
            "mensaje": f"Salida de {cantidad} unidades registrada",
            "producto": producto_actualizado
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/ajuste', methods=['POST'])
def ajustar_stock():
    """Ajusta stock a un valor específico (auditoría)."""
    try:
        datos = request.get_json()
        
        # Validar datos
        if 'producto_id' not in datos or 'nuevo_stock' not in datos:
            return jsonify({"error": "Faltan datos requeridos"}), 400
        
        producto_id = datos['producto_id']
        nuevo_stock = int(datos['nuevo_stock'])
        motivo = datos.get('motivo', 'Ajuste por auditoría')
        
        if nuevo_stock < 0:
            return jsonify({"error": "Stock no puede ser negativo"}), 400
        
        # Obtener producto actual
        producto = database.obtener_producto(producto_id)
        if not producto:
            return jsonify({"error": "Producto no encontrado"}), 404
        
        # Calcular diferencia para registrar
        diferencia = nuevo_stock - producto['stock']
        
        # Actualizar stock
        database.actualizar_stock(
            producto_id=producto_id,
            nuevo_stock=nuevo_stock,
            tipo='ajuste',
            cantidad=abs(diferencia),
            motivo=motivo
        )
        
        # Retornar producto actualizado
        producto_actualizado = database.obtener_producto(producto_id)
        return jsonify({
            "mensaje": f"Stock ajustado a {nuevo_stock} unidades",
            "producto": producto_actualizado
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ============================================================================
# API - CONSULTAS Y REPORTES
# ============================================================================

@app.route('/api/reporte', methods=['GET'])
def obtener_reporte():
    """Obtiene reporte de existencias."""
    try:
        reporte = database.obtener_reporte()
        return jsonify(reporte)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/historial', methods=['GET'])
def obtener_historial():
    """Obtiene historial de movimientos."""
    try:
        producto_id = request.args.get('producto_id')
        limite = int(request.args.get('limite', 100))
        
        movimientos = database.obtener_historial(producto_id, limite)
        return jsonify(movimientos)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/alertas', methods=['GET'])
def obtener_alertas():
    """Obtiene productos con alertas (stock bajo o agotado)."""
    try:
        productos = database.listar_productos()
        
        stock_bajo_list = [p for p in productos if p['stock'] <= p['stock_minimo'] and p['stock'] > 0]
        agotados_list = [p for p in productos if p['stock'] == 0]
        
        return jsonify({
            "total_productos": len(productos),
            "stock_bajo": len(stock_bajo_list),
            "agotados": len(agotados_list),
            "total_alertas": len(stock_bajo_list) + len(agotados_list),
            "productos_stock_bajo": stock_bajo_list,
            "productos_agotados": agotados_list
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ============================================================================
# API - ADMINISTRACIÓN (INICIALIZACIÓN Y LIMPIEZA)
# ============================================================================

@app.route('/api/inicializar', methods=['POST'])
def inicializar_datos():
    """
    Inicializa la BD con datos de demostración.
    Simula que el inventario viene de otro módulo.
    """
    try:
        productos = database.inicializar_datos_demo()
        return jsonify({
            "mensaje": f"✅ Base de datos inicializada con {len(productos)} productos",
            "productos": productos
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/limpiar', methods=['POST'])
def limpiar_datos():
    """
    Limpia toda la base de datos.
    ⚠️ ESTA ACCIÓN NO SE PUEDE DESHACER
    """
    try:
        if database.limpiar_base_datos():
            return jsonify({
                "mensaje": "✅ Base de datos limpiada correctamente"
            }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ============================================================================
# MANEJO DE ERRORES
# ============================================================================

@app.errorhandler(404)
def no_encontrado(error):
    return jsonify({"error": "No encontrado"}), 404


@app.errorhandler(500)
def error_servidor(error):
    return jsonify({"error": "Error interno del servidor"}), 500


# ============================================================================
# CICLO DE VIDA
# ============================================================================

@app.teardown_appcontext
def cerrar_bd(error):
    """Cierra conexión a BD al terminar."""
    if database.conn:
        database.desconectar()


if __name__ == '__main__':
    print("\n" + "="*70)
    print("  CONTROL DE EXISTENCIAS - Aplicacion Web")
    print("  Interfaz: http://localhost:5000")
    print("  Base de datos: PostgreSQL")
    print("="*70 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
