"""Clase SchemaInitializer - inicializa esquema de BD."""

from infrastructure.database.schema_initializer.crear_tablas import CrearTablasMixin


class SchemaInitializer(CrearTablasMixin):
    """
    Crear e INICIALIZAR el esquema de BD.
    
    Combina:
        • CrearTablasMixin - crear_tablas()
    
    RESPONSABILIDAD: 1
    • Ejecutar CREATE TABLE IF NOT EXISTS
    """
    
    def __init__(self, conn):
        """
        Inicializar con conexión existente.
        
        Args:
            conn: Conexión SQLite (de ConnectionManager)
        """
        self.conn = conn
