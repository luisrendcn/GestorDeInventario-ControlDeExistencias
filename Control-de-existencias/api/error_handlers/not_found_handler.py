"""
╔════════════════════════════════════════════════════════════════════════════╗
║                  ARCHIVO: api/error_handlers/not_found_handler.py          ║
║                  RESPONSABILIDAD: Manejar errores 404                      ║
╚════════════════════════════════════════════════════════════════════════════╝

🎯 ÚNICA RESPONSABILIDAD:
   Retornar respuesta JSON cuando un recurso no es encontrado (404).

📝 CASOS DE USO:
   • URL no existe en la aplicación
   • Producto no encontrado
   • Recurso eliminado o inexistente
"""

from flask import jsonify


def handle_not_found(error):
    """
    Retornar JSON con error 404.
    
    RESPONSABILIDAD: 1
    • Responder con JSON para errores 404
    
    Args:
        error: Excepción lanzada por Flask
        
    Returns:
        tuple: (JSON response, HTTP 404)
    """
    return jsonify({
        "error": "Recurso no encontrado",
        "codigo": 404,
    }), 404
