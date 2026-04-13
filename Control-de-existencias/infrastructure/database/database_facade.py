"""Database Facade - Agregador de servicios de BD."""

from infrastructure.database.connection_manager import ConnectionManager
from infrastructure.database.schema_initializer import SchemaInitializer
from infrastructure.database.query_executor import QueryExecutor
from infrastructure.database.query_reader import QueryReader
from infrastructure.database.database_cleaner import DatabaseCleaner


class Database:
    """
    Agregador de SERVICIOS DE BD (Facade Pattern).
    
    Combina todos los servicios de base de datos en una sola interfaz
    para proporcionar acceso conveniente a todas las operaciones.
    
    RESPONSABILIDAD: 1
    • Adaptar/agregar múltiples servicios BD atómicos en una interfaz unificada
    
    Internamente delega a:
        • ConnectionManager - ciclo de vida de conexión
        • SchemaInitializer - crear tablas
        • QueryExecutor - INSERT/UPDATE/DELETE
        • QueryReader - SELECT
        • DatabaseCleaner - limpiar BD
    """
    
    def __init__(self, db_path: str = "control_existencias.db"):
        """
        Inicializar el agregador con una ruta de BD.
        
        Args:
            db_path: Ruta al archivo SQLite
        """
        # Crear servicio de conexión
        self._connection_manager = ConnectionManager(db_path)
        
        # Los demás servicios se inicializan después de conectar
        self._schema_initializer = None
        self._query_executor = None
        self._query_reader = None
        self._database_cleaner = None
    
    @property
    def conn(self):
        """Acceso a conexión para servicios internos."""
        return self._connection_manager.conn
    
    # ============ MÉTODOS DELEGADOS: ConnectionManager ============
    
    def conectar(self):
        """Conectar a la BD."""
        self._connection_manager.conectar()
        
        # Inicializar otros servicios después de conectar
        self._schema_initializer = SchemaInitializer(self.conn)
        self._query_executor = QueryExecutor(self.conn)
        self._query_reader = QueryReader(self.conn)
        self._database_cleaner = DatabaseCleaner(self.conn)
    
    def desconectar(self):
        """Desconectar de la BD."""
        self._connection_manager.desconectar()
    
    def cerrar(self):
        """Alias para desconectar()."""
        self.desconectar()
    
    # ============ MÉTODOS DELEGADOS: SchemaInitializer ============
    
    def crear_tablas(self):
        """Crear tablas en la BD."""
        if self._schema_initializer:
            self._schema_initializer.crear_tablas()
    
    # ============ MÉTODOS DELEGADOS: QueryExecutor ============
    
    def ejecutar(self, query: str, params: tuple = ()):
        """Ejecutar query de modificación (INSERT/UPDATE/DELETE)."""
        if self._query_executor:
            return self._query_executor.ejecutar(query, params)
        raise RuntimeError("BD no conectada. Llamar a conectar() primero")
    
    # ============ MÉTODOS DELEGADOS: QueryReader ============
    
    def fetchone(self, query: str, params: tuple = ()):
        """Obtener un registro (SELECT)."""
        if self._query_reader:
            return self._query_reader.fetchone(query, params)
        raise RuntimeError("BD no conectada. Llamar a conectar() primero")
    
    def fetchall(self, query: str, params: tuple = ()):
        """Obtener todos los registros (SELECT)."""
        if self._query_reader:
            return self._query_reader.fetchall(query, params)
        raise RuntimeError("BD no conectada. Llamar a conectar() primero")
    
    # ============ MÉTODOS DELEGADOS: DatabaseCleaner ============
    
    def limpiar_base_datos(self) -> bool:
        """Limpiar toda la BD (IRREVERSIBLE)."""
        if self._database_cleaner:
            return self._database_cleaner.limpiar_base_datos()
        raise RuntimeError("BD no conectada. Llamar a conectar() primero")
