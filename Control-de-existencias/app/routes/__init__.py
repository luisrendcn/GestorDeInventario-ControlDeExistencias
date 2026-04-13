"""
╔════════════════════════════════════════════════════════════════╗
║  ARCHIVO: app/routes/__init__.py                              ║
║  FUNCIÓN: Orquestador de registro de rutas                    ║
╚════════════════════════════════════════════════════════════════╝

Centraliza el registro de todas las rutas simples (no blueprints).
"""

from app.routes.index_route import IndexRoute


class RoutesRegistry:
    """
    Registra todas las rutas simples de la aplicación.
    
    Rutas:
      • GET / - Página principal
    
    NOTA: Blueprints se registran aparte en BlueprintRegistry
    """
    
    def __init__(self, app):
        """Recibir aplicación Flask."""
        self.app = app
    
    def register_all(self):
        """Registrar todas las rutas."""
        print("[ROUTES] Registrando rutas...")
        
        # Registrar rutas
        IndexRoute(self.app).register()
        
        print("[ROUTES] ✅ Rutas registradas\n")
