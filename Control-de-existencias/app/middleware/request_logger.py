"""
╔════════════════════════════════════════════════════════════════╗
║  ARCHIVO: app/middleware/request_logger.py                    ║
║  FUNCIÓN: Loguear requests entrantes                          ║
╚════════════════════════════════════════════════════════════════╝

Middleware before_request: ejecuta antes de cada request.
"""

from flask import request


class RequestLogger:
    """
    Loguea información de cada request entrante.
    
    Responsabilidad:
      • Imprimir método + path + timestamp
      • Útil para debugging y auditoría
    """
    
    def __init__(self, app):
        """Recibir aplicación Flask."""
        self.app = app
    
    def register(self):
        """Registrar hook before_request."""
        @self.app.before_request
        def log_request():
            """Ejecutar antes de cada request."""
            self.handle_request()
        
        return self
    
    def handle_request(self):
        """
        Lógica de logging de request.
        
        Captura:
          • Método HTTP (GET, POST, etc)
          • Path de la ruta
          • User-Agent
        """
        print(f"[REQUEST] {request.method} {request.path}")
