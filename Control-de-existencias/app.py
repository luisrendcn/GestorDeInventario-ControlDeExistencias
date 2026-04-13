"""
╔════════════════════════════════════════════════════════════════╗
║  ARCHIVO: app.py                                               ║
║  FUNCIÓN: Punto de entrada refactorizado                      ║
╚════════════════════════════════════════════════════════════════╝

REFACTORIZACIÓN: La complejidad se ha movido a submódulos especializados:

  app/
  ├── __init__.py              → Factory create_app() + instancia global
  ├── application.py           → Clase FlaskApplication (FACADE)
  ├── database_initializer.py  → Inicialización de BD
  ├── blueprint_registry.py    → Registro de blueprints
  ├── middleware/
  │   ├── __init__.py         → MiddlewareRegistry (orquestador)
  │   ├── request_logger.py   → Logging de requests
  │   ├── response_handler.py → Manejo de responses
  │   ├── error_handler.py    → Captura de excepciones
  │   └── shutdown_handler.py → Limpieza al terminar
  └── routes/
      ├── __init__.py          → RoutesRegistry (orquestador)
      └── index_route.py       → Ruta GET /

BENEFICIOS:
  ✅ Separación de concerns (SRP - Single Responsibility Principle)
  ✅ Cada clase/método en su propio archivo
  ✅ Fácil de testear y mantener
  ✅ Escalable (agregar ruta nueva = agregar archivo)
  ✅ FACADE pattern conservado (FlaskApplication orquesta todo)
"""

from app import app, create_app
from config.settings import config


if __name__ == '__main__':
    """Punto de entrada del servidor."""
    print("\n" + "="*70)
    print("  ✨ CONTROL DE EXISTENCIAS - Sistema de Inventario")
    print("  🌐 Interfaz: http://localhost:5000")
    print("  📊 API V1: http://localhost:5000/api/v1")
    print("  💾 Base de datos: SQLite")
    print("="*70 + "\n")
    
    app.run(debug=config.DEBUG, host='0.0.0.0', port=5000)

