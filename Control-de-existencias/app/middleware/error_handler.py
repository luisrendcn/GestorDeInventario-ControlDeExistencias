"""
╔════════════════════════════════════════════════════════════════╗
║  ARCHIVO: app/middleware/error_handler.py                     ║
║  FUNCIÓN: Capturar y manejar excepciones                      ║
╚════════════════════════════════════════════════════════════════╝

Error handler global: ejecuta cuando hay excepciones no capturadas.
"""

from flask import jsonify
import traceback


class ErrorHandler:
    """
    Captura y maneja TODAS las excepciones.
    
    Responsabilidades:
      • Capturar excepciones no manejadas
      • Loguear detalles (tipo, mensaje, traceback)
      • Retornar JSON con error
    """
    
    def __init__(self, app):
        """Recibir aplicación Flask."""
        self.app = app
    
    def register(self):
        """Registrar error handler global."""
        @self.app.errorhandler(Exception)
        def handle_exception(error):
            """Ejecutar cuando hay excepción no capturada."""
            return self.handle_error(error)
        
        return self
    
    def handle_error(self, error):
        """
        Lógica de manejo de errores.
        
        Acciones:
          • Loguear tipo de excepción
          • Loguear mensaje
          • Loguear traceback completo
          • Retornar JSON al cliente
        """
        # Loguear completo
        print(f"[EXCEPTION_CATCHER] Caught exception: {type(error).__name__}: {str(error)}")
        traceback.print_exc()
        
        # Retornar respuesta JSON
        return jsonify({"error": str(error)}), 500
