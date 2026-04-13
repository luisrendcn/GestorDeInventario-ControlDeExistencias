"""
╔════════════════════════════════════════════════════════════════╗
║  ARCHIVO: app/blueprint_registry.py                           ║
║  FUNCIÓN: Registrar blueprints de API                         ║
╚════════════════════════════════════════════════════════════════╝

Orquesta el registro de todos los blueprints.
"""

from api import registrar_blueprints


class BlueprintRegistry:
    """
    Registra todos los blueprints (rutas de API).
    
    Blueprints:
      • Productos (CRUD)
      • Movimientos (Estrategias)
      • Reportes (Análisis)
      • Admin (Inicialización, limpieza)
    
    NOTA: Los blueprints están en api/v1/
    """
    
    def __init__(self, app):
        """Recibir aplicación Flask."""
        self.app = app
    
    def register_all(self):
        """Registrar todos los blueprints."""
        print("[BLUEPRINTS] Registrando blueprints...")
        
        try:
            registrar_blueprints(self.app)
            print("[BLUEPRINTS] ✅ Blueprints registrados exitosamente\n")
        except Exception as e:
            print(f"[BLUEPRINTS] ❌ Error: {e}")
            import traceback
            traceback.print_exc()
            raise
