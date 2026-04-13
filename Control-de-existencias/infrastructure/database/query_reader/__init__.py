"""Clase QueryReader - ejecuta queries de lectura."""

from infrastructure.database.query_reader.fetchone import FetchoneMixin
from infrastructure.database.query_reader.fetchall import FetchallMixin


class QueryReader(FetchoneMixin, FetchallMixin):
    """
    Ejecutar queries de LECTURA (SELECT).
    
    Combina:
        • FetchoneMixin - fetchone()
        • FetchallMixin - fetchall()
    
    RESPONSABILIDAD: 1
    • Ejecutar queries que LEEN datos
    """
    
    def __init__(self, conn):
        """
        Inicializar con conexión existente.
        
        Args:
            conn: Conexión SQLite (de ConnectionManager)
        """
        self.conn = conn
