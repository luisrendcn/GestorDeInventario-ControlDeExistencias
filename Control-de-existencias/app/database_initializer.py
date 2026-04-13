"""
╔════════════════════════════════════════════════════════════════╗
║  ARCHIVO: app/database_initializer.py                          ║
║  FUNCIÓN: Inicialización de BD y repositorios                 ║
╚════════════════════════════════════════════════════════════════╝

Responsabilidad única: Orquestar inicialización de:
  • Conexión SQLite
  • CreacIón de tablas
  • Inyección en singleton stores
"""

from config.settings import config
from infrastructure.database import ConnectionManager, SchemaInitializer
from infrastructure.repositories import DatabaseStore
from utils.db_connection import DatabaseConnection


class DatabaseInitializer:
    """
    Inicializa toda la infraestructura de base de datos.
    
    Responsabilidad:
      1. Crear conexión SQLite
      2. Crear tablas
      3. Inyectar conexión en stores
      4. Validar estado
    """
    
    def __init__(self, app):
        """Recibir aplicación Flask."""
        self.app = app
        self._connection_manager = None
    
    def initialize(self):
        """
        Ejecutar inicialización completa.
        
        Pasos:
            1. Inicializar DatabaseConnection singleton
            2. Crear y conectar ConnectionManager
            3. Crear tablas
            4. Inyectar en DatabaseStore
            5. Validar y loguear
        """
        print("[DB] Inicializando base de datos...")
        
        try:
            # Paso 1: DatabaseConnection robusto (con auto-reconnect)
            DatabaseConnection.init(str(config.DATABASE_PATH))
            print("[DB] ✓ DatabaseConnection singleton creado")
            
            # Paso 2: ConnectionManager
            self._connection_manager = ConnectionManager(str(config.DATABASE_PATH))
            self._connection_manager.conectar()
            print("[DB] ✓ Conectado a SQLite")
            
            # Paso 3: Crear tablas
            initializer = SchemaInitializer(self._connection_manager.conn)
            initializer.crear_tablas()
            print("[DB] ✓ Tablas creadas/verificadas")
            
            # Paso 4: Inyectar en stores
            DatabaseStore.set_database(self._connection_manager.conn)
            DatabaseStore.set_db_path(str(config.DATABASE_PATH))
            print("[DB] ✓ DatabaseStore configurado")
            
            # Paso 5: Log final
            print(f"✅ BD inicializada: {config.DATABASE_PATH}\n")
            
        except Exception as e:
            print(f"[DB] ❌ Error inicializando BD: {e}")
            import traceback
            traceback.print_exc()
            raise
