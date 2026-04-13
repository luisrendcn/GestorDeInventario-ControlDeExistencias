"""
╔════════════════════════════════════════════════════════════════════════════╗
║                  ARCHIVO: api/error_handlers/method_not_allowed_handler.py ║
║                  RESPONSABILIDAD: Manejar errores 405                      ║
╚════════════════════════════════════════════════════════════════════════════╝

🎯 ÚNICA RESPONSABILIDAD:
   Retornar respuesta JSON cuando se usa método HTTP no permitido (405).

📝 CASOS DE USO:
   • POST en endpoint que solo acepta GET
   • PUT en endpoint que solo acepta POST
   • DELETE en endpoint sin soporte DELETE
"""

from flask import jsonify


def handle_method_not_allowed(error):
    """
    Retornar JSON con error 405.
    
    RESPONSABILIDAD: 1
    • Responder con JSON para errores 405
    
    Args:
        error: Excepción lanzada por Flask
        
    Returns:
        tuple: (JSON response, HTTP 405)
    """
    return jsonify({
        "error": "Método no permitido",
        "codigo": 405,
    }), 405
