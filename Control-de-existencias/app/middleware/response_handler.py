"""
╔════════════════════════════════════════════════════════════════╗
║  ARCHIVO: app/middleware/response_handler.py                  ║
║  FUNCIÓN: Manejar responses y headers                         ║
╚════════════════════════════════════════════════════════════════╝

Middleware after_request: ejecuta después de cada response.
"""


class ResponseHandler:
    """
    Procesa cada response saliente.
    
    Responsabilidades:
      • Agregar headers de seguridad/control
      • Desactivar caché para actualizaciones inmediatas
      • Loguear status code de response
    """
    
    def __init__(self, app):
        """Recibir aplicación Flask."""
        self.app = app
    
    def register(self):
        """Registrar hook after_request."""
        @self.app.after_request
        def after_request(response):
            """Ejecutar después de cada response."""
            return self.handle_response(response)
        
        return self
    
    def handle_response(self, response):
        """
        Lógica de procesamiento de response.
        
        Acciones:
          • Loguear status code
          • Agregar headers anti-caché
          • Retornar response procesada
        """
        # Loguear
        print(f"[RESPONSE] Status: {response.status_code}")
        
        # Agregar headers para desactivar caché
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        
        return response
