"""
╔════════════════════════════════════════════════════════════════════════════╗
║                  ARCHIVO: api/v1/productos.py                             ║
║                  FUNCIÓN: Endpoints REST para CRUD de productos           ║
╚════════════════════════════════════════════════════════════════════════════╝

📋 RESPONSABILIDAD DEL ARCHIVO:
   Exponer endpoints HTTP REST para operaciones CRUD de productos.
   Convierte respuestas de servicios en JSON.

🎯 FUNCIONALIDADES:
   ✓ GET    /productos - Listar todos
   ✓ GET    /productos/<id> - Obtener uno
   ✓ POST   /productos - Crear
   ✓ DELETE /productos/<id> - Eliminar

═════════════════════════════════════════════════════════════════════════════

📦 FUNCIONES:

┌─ crear_productos_bp(service) - RESPONSABILIDADES: 1
│  ├─ Responsabilidad: Crear blueprint con todas las rutas CRUD
│  └─ Retorna: Blueprint configurado
│
├─ listar() - GET /productos - RESPONSABILIDADES: 1
│  ├─ Responsabilidad: Devolver lista de productos
│  ├─ Status: 200 (éxito), 500 (error)
│  └─ Response: Array de productos JSON
│
├─ obtener(producto_id) - GET /productos/<id> - RESPONSABILIDADES: 2
│  ├─ Responsabilidad 1: Validar que el producto existe
│  ├─ Responsabilidad 2: Retornar producto
│  ├─ Status: 200 (éxito), 404 (no encontrado), 500 (error)
│  └─ Response: Producto JSON o error
│
├─ crear() - POST /productos - RESPONSABILIDADES: 2
│  ├─ Responsabilidad 1: Validar datos de entrada
│  ├─ Responsabilidad 2: Retornar producto creado
│  ├─ Status: 201 (creado), 400 (datos inválidos), 500 (error)
│  └─ Body: {id, nombre, precio, stock, stock_minimo, descripcion}
│
└─ eliminar(producto_id) - DELETE /productos/<id> - RESPONSABILIDADES: 2
   ├─ Responsabilidad 1: Validar que el producto existe
   ├─ Responsabilidad 2: Eliminar y confirmar
   ├─ Status: 200 (éxito), 404 (no encontrado), 500 (error)
   └─ Response: Mensaje de confirmación o error

🚀 EJEMPLOS:

   # Listar
   GET  http://localhost:5000/api/v1/productos

   # Obtener
   GET  http://localhost:5000/api/v1/productos/P001

   # Crear
   POST http://localhost:5000/api/v1/productos
   Body: {"id": "P001", "nombre": "Laptop", "precio": 999.99, "stock": 10}

   # Eliminar
   DELETE http://localhost:5000/api/v1/productos/P001
"""

from flask import Blueprint, request, jsonify
from services.service_container import ServiceContainer
from core.exceptions import ProductoNoEncontrado, DatosInvalidos


def crear_productos_bp() -> Blueprint:
    """
    Crear blueprint de productos con 6 servicios atómicos.
    
    RESPONSABILIDADES: 1
    • Crear y retornar Blueprint configurado con todas las rutas CRUD
    
    Returns:
        Blueprint: Blueprint con 5 rutas (GET todos, GET uno, POST, UPDATE, DELETE)
    """
    bp = Blueprint('productos', __name__)
    
    @bp.route('/productos', methods=['GET'])
    def listar():
        """
        Listar todos los productos.
        
        RESPONSABILIDADES: 1
        • Retornar lista de todos los productos
        
        Returns:
            JSON array de productos
        
        Status:
          • 200: Éxito
          • 500: Error interno
        """
        try:
            service = ServiceContainer.get_listar_productos_service()
            productos = service.listar()
            print(f"[API] Productos listados: {len(productos)}")
            for p in productos:
                print(f"[API]   - {p}")
            return jsonify(productos), 200
        except Exception as e:
            print(f"[API ERROR] {str(e)}")
            return jsonify({"error": str(e)}), 500
    
    @bp.route('/productos/<producto_id>', methods=['GET'])
    def obtener(producto_id):
        """
        Obtener un producto por ID.
        
        RESPONSABILIDADES: 1
        • Retornar el producto
        
        Args:
            producto_id: ID del producto
        
        Returns:
            JSON del producto
        
        Status:
          • 200: Éxito
          • 404: Producto no encontrado
          • 500: Error interno
        """
        try:
            service = ServiceContainer.get_obtener_producto_service()
            producto = service.obtener(producto_id)
            return jsonify(producto.to_dict()), 200
        except ProductoNoEncontrado:
            return jsonify({"error": "Producto no encontrado"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @bp.route('/productos', methods=['POST'])
    def crear():
        """
        Crear un nuevo producto.
        
        RESPONSABILIDADES: 1
        • Crear y retornar producto creado
        
        Body JSON:
          • id: string (requerido)
          • nombre: string (requerido)
          • precio: float >= 0 (requerido)
          • stock: int >= 0 (requerido)
          • stock_minimo: int >= 0 (opcional, default 5)
          • descripcion: string (opcional)
        
        Returns:
            JSON del producto creado
        
        Status:
          • 201: Producto creado
          • 400: Datos inválidos
          • 500: Error interno
        """
        try:
            datos = request.get_json() or {}
            service = ServiceContainer.get_crear_producto_service()
            producto = service.crear(datos)
            return jsonify(producto), 201
        except DatosInvalidos as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @bp.route('/productos/<producto_id>', methods=['PUT'])
    def actualizar(producto_id):
        """
        Actualizar un producto existente.
        
        RESPONSABILIDADES: 1
        • Actualizar y retornar confirmación
        
        Args:
            producto_id: ID del producto
        
        Body JSON:
          Puede incluir cualquier campo (nombre, precio, stock, etc.)
        
        Returns:
            JSON con resultado
        
        Status:
          • 200: Actualizado exitosamente
          • 400: Datos inválidos
          • 404: Producto no encontrado
          • 500: Error interno
        """
        try:
            datos = request.get_json() or {}
            service = ServiceContainer.get_actualizar_producto_service()
            producto = service.actualizar(producto_id, datos)
            return jsonify(producto), 200
        except ProductoNoEncontrado:
            return jsonify({"error": "Producto no encontrado"}), 404
        except DatosInvalidos as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @bp.route('/productos/<producto_id>', methods=['DELETE'])
    def eliminar(producto_id):
        """
        Eliminar un producto.
        
        RESPONSABILIDADES: 1
        • Eliminar y confirmar
        
        Args:
            producto_id: ID del producto
        
        Returns:
            JSON con mensaje de confirmación
        
        Status:
          • 200: Eliminado exitosamente
          • 404: Producto no encontrado
          • 500: Error interno
        """
        try:
            service = ServiceContainer.get_eliminar_producto_service()
            resultado = service.eliminar(producto_id)
            return jsonify({"mensaje": "Producto eliminado correctamente"}), 200
        except ProductoNoEncontrado:
            return jsonify({"error": "Producto no encontrado"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @bp.route('/productos/buscar/<nombre>', methods=['GET'])
    def buscar(nombre):
        """
        Buscar productos por nombre.
        
        RESPONSABILIDADES: 1
        • Buscar y retornar resultados
        
        Args:
            nombre: Nombre (o parte) a buscar
        
        Returns:
            JSON array de productos encontrados
        
        Status:
          • 200: Éxito (puede retornar array vacío)
          • 500: Error interno
        """
        try:
            service = ServiceContainer.get_buscar_producto_service()
            productos = service.buscar_por_nombre(nombre)
            return jsonify(productos), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    return bp
