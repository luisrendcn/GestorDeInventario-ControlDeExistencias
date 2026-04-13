"""
╔════════════════════════════════════════════════════════════════╗
║  ARCHIVO: app/routes/index_route.py                           ║
║  FUNCIÓN: Ruta principal (página índice)                      ║
╚════════════════════════════════════════════════════════════════╝

Define la ruta GET / que sirve la página principal.
"""

from flask import render_template


class IndexRoute:
    """
    Ruta principal de la aplicación.
    
    Responsabilidad:
      • Registrar ruta GET /
      • Servir plantilla index.html
    """
    
    def __init__(self, app):
        """Recibir aplicación Flask."""
        self.app = app
    
    def register(self):
        """Registrar la ruta."""
        @self.app.route('/')
        def index():
            """Servir página principal."""
            return self.handle_index()
        
        return self
    
    def handle_index(self):
        """
        Lógica de la ruta /.
        
        Returns:
          HTML renderizado desde plantilla index.html
        """
        return render_template('index.html')
