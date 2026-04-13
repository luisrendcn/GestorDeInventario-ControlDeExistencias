"""
╔════════════════════════════════════════════════════════════════╗
║  ARCHIVO: app/application.py                                   ║
║  FUNCIÓN: Clase FlaskApplication - Orquestador principal      ║
╚════════════════════════════════════════════════════════════════╝

Implementa el FACADE PATTERN coordinando todos los subsistemas:
  • Inicialización de BD
  • Registro de middlewares
  • Registro de blueprints
  • Gestión de ciclo de vida
"""

from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

from config.settings import config
from app.database_initializer import DatabaseInitializer
from app.middleware import MiddlewareRegistry
from app.routes import RoutesRegistry
from app.blueprint_registry import BlueprintRegistry


class FlaskApplication:
    """
    Clase principal que actúa como FACADE.
    
    Responsabilidades:
      1. Crear y configurar aplicación Flask
      2. Orquestar inicialización de BD
      3. Registrar middlewares
      4. Registrar rutas
      5. Registrar blueprints
    
    Usa composición y Mixins para mantener separación de concerns.
    """
    
    def __init__(self):
        """Inicializar aplicación."""
        # Cargar variables de entorno
        load_dotenv()
        
        # Crear instancia Flask
        self.app = Flask(__name__)
        self.app.config.from_object(config)
        CORS(self.app, origins=config.CORS_ORIGINS)
    
    def initialize(self):
        """
        Orquestar inicialización completa de la aplicación.
        
        Flujo:
            1. Inicializar BD y repositorios
            2. Registrar middlewares (before/after/error)
            3. Registrar rutas simples (/)
            4. Registrar blueprints (API)
        """
        # Paso 1: Inicializar BD
        db_initializer = DatabaseInitializer(self.app)
        db_initializer.initialize()
        
        # Paso 2: Registrar middlewares
        middleware_registry = MiddlewareRegistry(self.app)
        middleware_registry.register_all()
        
        # Paso 3: Registrar rutas
        routes_registry = RoutesRegistry(self.app)
        routes_registry.register_all()
        
        # Paso 4: Registrar blueprints
        blueprint_registry = BlueprintRegistry(self.app)
        blueprint_registry.register_all()
        
        return self.app
    
    def run(self, debug=None, host='0.0.0.0', port=5000):
        """Correr el servidor Flask."""
        if debug is None:
            debug = config.DEBUG
        
        self._print_startup_banner()
        self.app.run(debug=debug, host=host, port=port)
    
    @staticmethod
    def _print_startup_banner():
        """Imprimir banner de inicio."""
        print("\n" + "="*70)
        print("  ✨ CONTROL DE EXISTENCIAS - Sistema de Inventario")
        print("  🌐 Interfaz: http://localhost:5000")
        print("  📊 API V1: http://localhost:5000/api/v1")
        print("  💾 Base de datos: SQLite")
        print("="*70 + "\n")
