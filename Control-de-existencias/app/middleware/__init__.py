"""
╔════════════════════════════════════════════════════════════════╗
║  ARCHIVO: app/middleware/__init__.py                           ║
║  FUNCIÓN: Orquestador de registro de middlewares              ║
╚════════════════════════════════════════════════════════════════╝

Centraliza el registro de todos los middlewares.
"""

from app.middleware.request_logger import RequestLogger
from app.middleware.response_handler import ResponseHandler
from app.middleware.error_handler import ErrorHandler
from app.middleware.shutdown_handler import ShutdownHandler


class MiddlewareRegistry:
    """
    Registra todos los middlewares de la aplicación.
    
    Middlewares:
      • RequestLogger - Loguea requests entrantes
      • ResponseHandler - Maneja responses (headers, caché)
      • ErrorHandler - Captura excepciones
      • ShutdownHandler - Limpieza al terminar request
    """
    
    def __init__(self, app):
        """Recibir aplicación Flask."""
        self.app = app
    
    def register_all(self):
        """Registrar todos los middlewares."""
        print("[MIDDLEWARE] Registrando middlewares...")
        
        # Registrar en orden de ejecución
        RequestLogger(self.app).register()
        ResponseHandler(self.app).register()
        ErrorHandler(self.app).register()
        ShutdownHandler(self.app).register()
        
        print("[MIDDLEWARE] ✅ Todos los middlewares registrados\n")
