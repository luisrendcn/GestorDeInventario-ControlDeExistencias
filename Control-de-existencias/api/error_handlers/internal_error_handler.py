"""
╔════════════════════════════════════════════════════════════════════════════╗
║                  ARCHIVO: api/error_handlers/internal_error_handler.py     ║
║                  RESPONSABILIDAD: Manejar errores 500                      ║
╚════════════════════════════════════════════════════════════════════════════╝

🎯 ÚNICA RESPONSABILIDAD:
   Retornar respuesta JSON cuando hay error interno del servidor (500).

📝 CASOS DE USO:
   • Excepciones no capturadas en endpoints
   • Errores de conexión a base de datos
   • Errores inesperados en lógica de negocio
"""

from flask import jsonify


def handle_internal_error(error):
    """
    Retornar JSON con error 500.
    
    RESPONSABILIDAD: 1
    • Responder con JSON para errores 500
    
    Args:
        error: Excepción lanzada en la aplicación
        
    Returns:
        tuple: (JSON response, HTTP 500)
    """
    print(f"[ERROR_HANDLER] Internal error caught: {type(error).__name__}: {str(error)}")
    import traceback
    traceback.print_exc()
    
    return jsonify({
        "error": "Error interno del servidor",
        "detalle": str(error),
        "codigo": 500,
    }), 500
