"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                  ARCHIVO: api/v1/movimientos.py                             ║
║       FUNCIÓN: Endpoints REST para movimientos de stock (STRATEGY)     ║
╚═══════════════════════════════════════════════════════════════════════════════╝

📊 RESPONSABILIDAD DEL ARCHIVO:
   Exponer endpoints HTTP REST que implementan el STRATEGY PATTERN
   para manejo de movimientos de stock (entrada/salida/ajuste).

🎯 FUNCIONALIDADES:
   ✓ POST /entrada - Entrada de stock (suma sin validar máximo)
   ✓ POST /salida - Salida de stock (resta con validación)
   ✓ POST /ajuste - Ajuste de stock (asigna valor exacto)

═══════════════════════════════════════════════════════════════════════════════

📊 FUNCIONES:

┌─ crear_movimientos_bp(service) - RESPONSABILIDADES: 1
├─ Responsabilidad: Crear blueprint con las 3 estrategias
└─ Retorna: Blueprint configurado

┌─ entrada() - POST /entrada - RESPONSABILIDADES: 2
├─ Responsabilidad 1: Validar datos de entrada
├─ Responsabilidad 2: Llamar estrategia ENTRADA
└─ Status: 200 (éxito), 400 (datos inválidos), 404 (no encontrado), 500 (error)

┌─ salida() - POST /salida - RESPONSABILIDADES: 3
├─ Responsabilidad 1: Validar datos de entrada
├─ Responsabilidad 2: Validar stock disponible
├─ Responsabilidad 3: Llamar estrategia SALIDA
└─ Status: 200 (éxito), 400 (inválido/insuficiente), 404 (no encontrado), 500 (error)

┌─ ajuste() - POST /ajuste - RESPONSABILIDADES: 2
├─ Responsabilidad 1: Validar datos de entrada
├─ Responsabilidad 2: Llamar estrategia AJUSTE
└─ Status: 200 (éxito), 400 (datos inválidos), 404 (no encontrado), 500 (error)

🚀 EJEMPLOS:

   # Entrada: Compra a proveedor (suma 50 unidades)
   POST http://localhost:5000/api/v1/entrada
   Body: {"producto_id": "P001", "cantidad": 50, "motivo": "Compra a proveedor"}

   # Salida: Venta a cliente (resta 10 unidades)
   POST http://localhost:5000/api/v1/salida
   Body: {"producto_id": "P001", "cantidad": 10, "motivo": "Venta"}

   # Ajuste: Auditoría física (asigna valor exacto)
   POST http://localhost:5000/api/v1/ajuste
   Body: {"producto_id": "P001", "nuevo_stock": 42, "motivo": "Auditoría física"}
"""

from flask import Blueprint, request, jsonify
from services.service_container import ServiceContainer
from core.exceptions import (
    ProductoNoEncontrado,
    StockInsuficiente,
    DatosInvalidos,
)


def crear_movimientos_bp() -> Blueprint:
    """
    Crear blueprint de movimientos con 3 estrategias atómicas.
    
    RESPONSABILIDADES: 1
    • Crear y retornar Blueprint configurado con las 3 estrategias
    
    Returns:
        Blueprint: Blueprint con 3 rutas (entrada, salida, ajuste)
    """
    bp = Blueprint('movimientos', __name__)
    
    @bp.route('/entrada', methods=['POST'])
    def entrada():
        """
        Registrar entrada de stock.
        
        ESTRATEGIA 1: ENTRADA - Suma stock sin validar máximo
        
        RESPONSABILIDADES: 1
        • Registrar entrada y confirmar
        
        Body JSON requerido:
          • producto_id: string (requerido)
          • cantidad: int > 0 (requerido)
          • motivo: string (opcional, default 'Entrada')
        
        Returns:
            JSON con resultado del movimiento
        
        Status:
          • 200: Entrada registrada
          • 400: Datos inválidos
          • 404: Producto no encontrado
          • 500: Error interno
        """
        try:
            datos = request.get_json() or {}
            strategy = ServiceContainer.get_entrada_strategy()
            resultado = strategy.ejecutar(
                producto_id=datos.get('producto_id'),
                cantidad=int(datos.get('cantidad', 0)),
                motivo=datos.get('motivo', 'Entrada'),
            )
            return jsonify({
                "mensaje": "✅ Entrada de stock registrada",
                "movimiento": resultado
            }), 200
        except ProductoNoEncontrado as e:
            return jsonify({"error": str(e)}), 404
        except (DatosInvalidos, ValueError) as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @bp.route('/salida', methods=['POST'])
    def salida():
        """
        Registrar salida de stock.
        
        ESTRATEGIA 2: SALIDA - Resta stock CON validación de disponibilidad
        
        RESPONSABILIDADES: 1
        • Registrar salida (con validación) y confirmar
        
        Body JSON requerido:
          • producto_id: string (requerido)
          • cantidad: int > 0 (requerido)
          • motivo: string (opcional, default 'Salida')
        
        Returns:
            JSON con resultado del movimiento
        
        Status:
          • 200: Salida registrada
          • 400: Datos inválidos o stock insuficiente
          • 404: Producto no encontrado
          • 500: Error interno
        """
        try:
            datos = request.get_json() or {}
            strategy = ServiceContainer.get_salida_strategy()
            resultado = strategy.ejecutar(
                producto_id=datos.get('producto_id'),
                cantidad=int(datos.get('cantidad', 0)),
                motivo=datos.get('motivo', 'Salida'),
            )
            return jsonify({
                "mensaje": "✅ Salida de stock registrada",
                "movimiento": resultado
            }), 200
        except ProductoNoEncontrado as e:
            return jsonify({"error": str(e)}), 404
        except StockInsuficiente as e:
            return jsonify({"error": f"❌ {str(e)}"}), 400
        except (DatosInvalidos, ValueError) as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @bp.route('/ajuste', methods=['POST'])
    def ajuste():
        """
        Ajustar stock a un valor específico.
        
        ESTRATEGIA 3: AJUSTE - Asigna valor exacto (para auditoría)
        
        RESPONSABILIDADES: 1
        • Registrar ajuste y confirmar
        
        Body JSON requerido:
          • producto_id: string (requerido)
          • nuevo_stock: int >= 0 (requerido)
          • motivo: string (opcional, default 'Ajuste')
        
        Returns:
            JSON con resultado del movimiento
        
        Status:
          • 200: Ajuste registrado
          • 400: Datos inválidos
          • 404: Producto no encontrado
          • 500: Error interno
        """
        try:
            datos = request.get_json() or {}
            strategy = ServiceContainer.get_ajuste_strategy()
            resultado = strategy.ejecutar(
                producto_id=datos.get('producto_id'),
                nuevo_stock=int(datos.get('nuevo_stock', 0)),
                motivo=datos.get('motivo', 'Ajuste por auditoría'),
            )
            return jsonify({
                "mensaje": "✅ Stock ajustado correctamente",
                "producto": resultado
            }), 200
        except ProductoNoEncontrado as e:
            return jsonify({"error": str(e)}), 404
        except (DatosInvalidos, ValueError) as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    return bp
