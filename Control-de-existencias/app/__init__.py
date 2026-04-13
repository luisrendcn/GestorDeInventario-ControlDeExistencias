"""
╔════════════════════════════════════════════════════════════════╗
║  ARCHIVO: app/__init__.py                                      ║
║  FUNCIÓN: Punto de entrada - exportar aplicación Flask        ║
╚════════════════════════════════════════════════════════════════╝

Este archivo:
  1. Crea la aplicación Flask
  2. La inicializa completamente
  3. La exporta para uso en run.py
"""

from app.application import FlaskApplication


def create_app():
    """
    Factory function para crear la aplicación Flask.
    
    Implementa todos los pasos de inicialización:
      1. Crear instancia FlaskApplication
      2. Inicializar (BD, middlewares, rutas, blueprints)
      3. Retornar app lista para usar
    
    Returns:
      app (Flask): Aplicación completamente inicializada
    
    Ejemplo de uso:
      from app import create_app
      app = create_app()
      app.run()
    """
    flask_app = FlaskApplication()
    return flask_app.initialize()


# Crear instancia global para compatibilidad con run.py
app = create_app()
