"""
╔════════════════════════════════════════════════════════════════╗
║  ARCHIVO: app.py                                               ║
║  FUNCIÓN: Aplicación Flask - Orquestador principal            ║
╚════════════════════════════════════════════════════════════════╝

📋 RESPONSABILIDADES DEL ARCHIVO:
  • Crear y configurar aplicación Flask
  • Inicializar infraestructura (BD, repositorios, factories)
  • Registrar blueprints (APIs y endpoints HTTP)
  • Gestionar ciclo de vida (startup, shutdown)
  • Implementar FACADE PATTERN para coordinar subsistemas

🏛️  ARQUITECTURA LIMPIA (Clean Architecture):
  
  config/          → Configuración centralizada por ambiente
  core/            → Modelos, esquemas, excepciones (sin dependencias)
  infrastructure/  → BD, repositorios (acceso a datos)
  services/        → Lógica de negocio (ProductoService, etc)
  api/v1/          → Blueprints y rutas HTTP
  static/          → Archivos estáticos (JS, CSS)
  templates/       → Plantillas HTML
  utils/           → Utilidades

🏭 PATRÓN FACADE EN app.py:
  
  El punto de entrada (app.py) orquesta la complejidad de subsistemas:
    ├─ infrastructure.Database (conexión SQLite)
    ├─ infrastructure.RepositorioFactory (factory de repos)
    ├─ api.registrar_blueprints (rutas HTTP)
    └─ services.* (toda la lógica de negocio)
  
  Beneficios:
    • Punto de entrada único y limpio
    • Oculta la complejidad interna
    • Facilita testing y mantenimiento
    • Desacopla inicialización del resto
"""

from flask import Flask, render_template
from flask_cors import CORS
from dotenv import load_dotenv

from config.settings import config
from infrastructure.database import ConnectionManager, SchemaInitializer
from infrastructure.repositories import DatabaseStore, RepositorioFactory, MovimientoRepositoryFactory
from api import registrar_blueprints
from utils.db_connection import DatabaseConnection

# Cargar variables de entorno
load_dotenv()

# Crear aplicación Flask
app = Flask(__name__)
app.config.from_object(config)
CORS(app, origins=config.CORS_ORIGINS)

# Instancia global del gestor de conexión (para acceso desde middleware)
_connection_manager = None


# ============================================================================
# INICIALIZACIÓN
# ============================================================================

def init_database():
    """
    Inicializar base de datos y repositorios.
    """
    global _connection_manager
    
    # Inicializar DatabaseConnection robusto
    DatabaseConnection.init(str(config.DATABASE_PATH))
    
    _connection_manager = ConnectionManager(str(config.DATABASE_PATH))
    _connection_manager.conectar()
    
    # Inicializar esquema (crear tablas si no existen)
    initializer = SchemaInitializer(_connection_manager.conn)
    initializer.crear_tablas()
    
    # Inyectar conexión en el Store (para FACTORY METHOD PATTERN)
    DatabaseStore.set_database(_connection_manager.conn)
    DatabaseStore.set_db_path(str(config.DATABASE_PATH))
    
    print(f"✅ BD inicializada: {config.DATABASE_PATH}")


# Inicializar BD al crear la app
init_database()

# ============================================================================
# MIDDLEWARE - CICLO DE VIDA (parte del FACADE)
# ============================================================================

@app.before_request
def log_request():
    """Log incoming requests."""
    print(f"[REQUEST] {__import__('flask').request.method} {__import__('flask').request.path}")

@app.after_request  
def after_request(response):
    """Log after request is processed and disable caching."""
    print(f"[RESPONSE] Status: {response.status_code}")
    # Desactivar caché para asegurar actualizaciones inmediatas
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.errorhandler(Exception)
def handle_all_exceptions(error):
    """Catch ALL exceptions including import errors."""
    print(f"[EXCEPTION_CATCHER] Caught exception: {type(error).__name__}: {str(error)}")
    import traceback
    traceback.print_exc()
    from flask import jsonify
    return jsonify({"error": str(error)}), 500

@app.teardown_appcontext
def shutdown(exception):
    """
    Limpieza al terminar el request (parte del FACADE PATTERN).
    
    NOTA: NO desconectamos aquí porque Flask ejecuta teardown_appcontext
    al final de CADA REQUEST, lo que causaría que la conexión se cierre
    y esté indisponible para los siguientes requests.
    
    La conexión se mantendrá abierta durante toda la vida de la aplicación
    y solo se cerrará cuando Flask se apague completamente.
    """
    # Mantener conexión abierta durante la vida de la aplicación
    pass


# ============================================================================
# RUTAS - PÁGINA PRINCIPAL
# ============================================================================

@app.route('/')
def index():
    """Página principal."""
    return render_template('index.html')


# ============================================================================
# REGISTRO DE BLUEPRINTS (API) - Parte del FACADE
# ============================================================================
# El FACADE registra todos los blueprints y centraliza el enrutamiento.
# Esto mantiene la aplicación principal limpia y desacoplada de rutas específicas.

print("[APP] Registrando blueprints...")
try:
    registrar_blueprints(app)
    print("[APP] ✅ Blueprints registrados exitosamente")
except Exception as e:
    print(f"[APP] ❌ Error registrando blueprints: {e}")
    import traceback
    traceback.print_exc()
    raise


# ============================================================================
# PUNTO DE ENTRADA
# ============================================================================

if __name__ == '__main__':
    print("\n" + "="*70)
    print("  ✨ CONTROL DE EXISTENCIAS - Sistema de Inventario")
    print("  🌐 Interfaz: http://localhost:5000")
    print("  📊 API V1: http://localhost:5000/api/v1")
    print("  💾 Base de datos: SQLite")
    print("="*70 + "\n")
    
    app.run(debug=config.DEBUG, host='0.0.0.0', port=5000)
