"""
╔════════════════════════════════════════════════════════════════════════════╗
║                  ARCHIVO: api/__init__.py                                 ║
║                  RESPONSABILIDAD: Coordinador central de blueprints       ║
╚════════════════════════════════════════════════════════════════════════════╝

🎯 ÚNICA RESPONSABILIDAD:
   Registrar todos los blueprints (rutas) y manejadores de errores
   en la aplicación Flask centralmente.

💡 ESTRUCTURA:
   • Blueprints V1: 4 blueprints con rutas específicas
   • Error Handlers: 4 handlers para códigos HTTP (400, 404, 405, 500)

🔗 ARQUITECTURA:

   app.py
     ↓
   registrar_blueprints(app)
     ├─ crear_blueprints_v1(app) → Registra 4 blueprints
     └─ registrar_error_handlers(app) → Registra 4 manejadores

📊 RUTAS TOTALES:
   • /api/v1/productos (5 rutas CRUD)
   • /api/v1/movimientos (3 rutas Strategy)
   • /api/v1/reportes (5 rutas de análisis)
   • /api/v1/admin (2 rutas de admin)
   • Handlers de error (404, 500, 405, 400)
"""

from flask import Flask
from .v1 import crear_blueprints_v1
from api.error_handlers import (
    handle_not_found,
    handle_internal_error,
    handle_method_not_allowed,
    handle_bad_request,
)


def registrar_error_handlers(app: Flask) -> None:
    """
    Registrar manejadores de errores HTTP globales.
    
    RESPONSABILIDAD: 1
    • Registrar 4 handlers para códigos de error (400, 404, 405, 500)
    
    Args:
        app: Instancia de Flask
    """
    app.errorhandler(404)(handle_not_found)
    app.errorhandler(500)(handle_internal_error)
    app.errorhandler(405)(handle_method_not_allowed)
    app.errorhandler(400)(handle_bad_request)


def registrar_blueprints(app: Flask) -> None:
    """
    Registrar todos los blueprints en la aplicación.
    
    RESPONSABILIDAD: 1
    • Coordinar el registro de blueprints y error handlers
    
    Args:
        app: Instancia de Flask para registrar blueprints
    """
    # Blueprints V1 (rutas de API)
    crear_blueprints_v1(app)
    
    # Error handlers (manejadores de errores HTTP)
    registrar_error_handlers(app)


__all__ = ['registrar_blueprints']
