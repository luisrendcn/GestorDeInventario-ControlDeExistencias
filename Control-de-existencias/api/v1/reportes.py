"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                  ARCHIVO: api/v1/reportes.py                               ║
║         FUNCIÓN: Endpoints REST para reportes y análisis              ║
╚══════════════════════════════════════════════════════════════════════════════╝

📊 RESPONSABILIDAD DEL ARCHIVO:
   Exponer endpoints HTTP REST para generar reportes y análisis
   del estado del inventario.

🎯 FUNCIONALIDADES:
   ✓ GET /reporte - Reporte general del inventario
   ✓ GET /alertas - Alertas de stock bajo/agotados
   ✓ GET /historial - Historial de movimientos
   ✓ GET /productos-mayor-stock - Top 5 con mayor stock
   ✓ GET /productos-menor-stock - Top 5 con menor stock

═══════════════════════════════════════════════════════════════════════════════

📊 FUNCIONES:

┌─ crear_reportes_bp(service) - RESPONSABILIDADES: 1
├─ Responsabilidad: Crear blueprint con 5 rutas de reportes
└─ Retorna: Blueprint configurado

┌─ reporte() - GET /reporte - RESPONSABILIDADES: 1
├─ Responsabilidad: Retornar estadísticas globales
└─ Status: 200 (éxito), 500 (error)

┌─ alertas() - GET /alertas - RESPONSABILIDADES: 1
├─ Responsabilidad: Retornar productos en alerta
└─ Status: 200 (éxito), 500 (error)

┌─ historial() - GET /historial?producto_id&limite - RESPONSABILIDADES: 2
├─ Responsabilidad 1: Validar parámetros
├─ Responsabilidad 2: Retornar movimientos filtrados
└─ Status: 200 (éxito), 400 (parámetro inválido), 500 (error)

┌─ mayor_stock() - GET /productos-mayor-stock?limite - RESPONSABILIDADES: 2
├─ Responsabilidad 1: Validar parámetro
├─ Responsabilidad 2: Retornar top N ordenados
└─ Status: 200 (éxito), 400 (parámetro inválido), 500 (error)

┌─ menor_stock() - GET /productos-menor-stock?limite - RESPONSABILIDADES: 2
├─ Responsabilidad 1: Validar parámetro
├─ Responsabilidad 2: Retornar bottom N ordenados
└─ Status: 200 (éxito), 400 (parámetro inválido), 500 (error)

🚀 EJEMPLOS:

   # Reporte general
   GET http://localhost:5000/api/v1/reporte

   # Alertas
   GET http://localhost:5000/api/v1/alertas

   # Historial completo
   GET http://localhost:5000/api/v1/historial

   # Historial de un producto
   GET http://localhost:5000/api/v1/historial?producto_id=P001

   # Top 10 mayor stock
   GET http://localhost:5000/api/v1/productos-mayor-stock?limite=10

   # Top 5 menor stock (default)
   GET http://localhost:5000/api/v1/productos-menor-stock
"""

from flask import Blueprint, request, jsonify
from services.service_container import ServiceContainer


def crear_reportes_bp() -> Blueprint:
    """
    Crear blueprint de reportes con 6 servicios atómicos.
    
    RESPONSABILIDADES: 1
    - Crear y retornar Blueprint configurado con 6 rutas de reportes
    
    Returns:
        Blueprint: Blueprint con 6 rutas de reportes
    """
    bp = Blueprint('reportes', __name__)
    
    @bp.route('/reporte', methods=['GET'])
    def reporte():
        """
        Obtener reporte general del inventario.
        
        RESPONSABILIDADES: 1
        • Calcular y retornar estadísticas globales
        
        Returns:
            JSON con estadísticas del inventario
        
        Status:
          • 200: Éxito
          • 500: Error interno
        """
        try:
            service = ServiceContainer.get_reporte_general_service()
            data = service.generar()
            return jsonify(data), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @bp.route('/alertas', methods=['GET'])
    def alertas():
        """
        Obtener alertas de stock.
        
        RESPONSABILIDADES: 1
        • Identificar y retornar productos en alerta
        
        Returns:
            JSON con alertas de stock bajo y agotados
        
        Status:
          • 200: Éxito
          • 500: Error interno
        """
        try:
            service = ServiceContainer.get_alertas_service()
            data = service.generar()
            return jsonify(data), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @bp.route('/historial', methods=['GET'])
    def historial():
        """
        Obtener historial de movimientos.
        
        RESPONSABILIDADES: 1
        • Retornar movimientos filtrados
        
        Query Parameters (opcional):
          • producto_id: Filtrar por producto (opcional)
          • limite: Máximo de registros (default 100)
        
        Returns:
            JSON con movimientos del historial
        
        Status:
          • 200: Éxito
          • 400: Parámetro inválido
          • 500: Error interno
        """
        try:
            producto_id = request.args.get('producto_id')
            limite = int(request.args.get('limite', 100))
            
            service = ServiceContainer.get_historial_service()
            data = service.generar(producto_id, limite)
            return jsonify(data), 200
        except ValueError:
            return jsonify({"error": "Parámetro límite inválido"}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @bp.route('/productos-mayor-stock', methods=['GET'])
    def mayor_stock():
        """
        Obtener productos con mayor stock.
        
        RESPONSABILIDADES: 1
        • Retornar top N ordenados descendente
        
        Query Parameters (opcional):
          • limite: Cantidad de productos (default 10)
        
        Returns:
            JSON array de productos ordenados por stock descendente
        
        Status:
          • 200: Éxito
          • 400: Parámetro inválido
          • 500: Error interno
        """
        try:
            limite = int(request.args.get('limite', 10))
            service = ServiceContainer.get_productos_mayor_stock_service()
            data = service.generar(limite)
            return jsonify(data), 200
        except ValueError:
            return jsonify({"error": "Parámetro límite inválido"}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @bp.route('/productos-menor-stock', methods=['GET'])
    def menor_stock():
        """
        Obtener productos con menor stock.
        
        RESPONSABILIDADES: 1
        • Retornar bottom N ordenados ascendente
        
        Query Parameters (opcional):
          • limite: Cantidad de productos (default 10)
        
        Returns:
            JSON array de productos ordenados por stock ascendente
        
        Status:
          • 200: Éxito
          • 400: Parámetro inválido
          • 500: Error interno
        """
        try:
            limite = int(request.args.get('limite', 10))
            service = ServiceContainer.get_productos_menor_stock_service()
            data = service.generar(limite)
            return jsonify(data), 200
        except ValueError:
            return jsonify({"error": "Parámetro límite inválido"}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @bp.route('/valuacion', methods=['GET'])
    def valuacion():
        """
        Obtener valuación económica del inventario.
        
        RESPONSABILIDADES: 1
        • Calcular y retornar valor total del inventario
        
        Returns:
            JSON con valuación por producto, categoría y total
        
        Status:
          • 200: Éxito
          • 500: Error interno
        """
        try:
            service = ServiceContainer.get_valuation_service()
            data = service.generar()
            return jsonify(data), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    return bp
