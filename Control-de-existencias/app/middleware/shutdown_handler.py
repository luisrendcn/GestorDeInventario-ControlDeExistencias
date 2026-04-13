"""
╔════════════════════════════════════════════════════════════════╗
║  ARCHIVO: app/middleware/shutdown_handler.py                  ║
║  FUNCIÓN: Limpiar recursos al finalizar request               ║
╚════════════════════════════════════════════════════════════════╝

Middleware teardown_appcontext: ejecuta al finalizar cada request.
"""


class ShutdownHandler:
    """
    Limpia recursos al finalizar cada request.
    
    Responsabilidades:
      • Cerrar conexiones si es necesario
      • Liberar recursos
      • Hacer cleanup general
    
    NOTA: NO cerramos conexión de BD aquí porque Flask ejecuta
    teardown_appcontext al final de CADA REQUEST, causando que
    la conexión se cierre y esté indisponible para siguientes requests.
    
    La conexión se mantiene abierta durante toda la vida de la app.
    """
    
    def __init__(self, app):
        """Recibir aplicación Flask."""
        self.app = app
    
    def register(self):
        """Registrar hook teardown_appcontext."""
        @self.app.teardown_appcontext
        def teardown(exception):
            """Ejecutar al finalizar cada request."""
            self.handle_shutdown(exception)
        
        return self
    
    def handle_shutdown(self, exception):
        """
        Lógica de limpieza.
        
        Args:
          exception: Excepción si ocurrió durante request (None si fue exitoso)
        
        Acciones:
          • Log de información
          • Cleanup de recursos
          • MANTENER conexión BD abierta
        """
        # Por ahora, solo mantener asignación vacía
        # La conexión BD se mantiene abierta
        pass
