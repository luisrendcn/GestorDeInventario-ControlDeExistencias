"""
╔════════════════════════════════════════════════════════════════════════════╗
║                  ARCHIVO: api/error_handlers/bad_request_handler.py        ║
║                  RESPONSABILIDAD: Manejar errores 400                      ║
╚════════════════════════════════════════════════════════════════════════════╝

🎯 ÚNICA RESPONSABILIDAD:
   Retornar respuesta JSON cuando hay solicitud inválida (400).

📝 CASOS DE USO:
   • JSON malformado en body
   • Parámetros requeridos faltantes
   • Formato de datos inválido
"""

from flask import jsonify


def handle_bad_request(error):
    """
    Retornar JSON con error 400.
    
    RESPONSABILIDAD: 1
    • Responder con JSON para errores 400
    
    Args:
        error: Excepción lanzada por Flask
        
    Returns:
        tuple: (JSON response, HTTP 400)
    """
    return jsonify({
        "error": "Solicitud inválida",
        "codigo": 400,
    }), 400
