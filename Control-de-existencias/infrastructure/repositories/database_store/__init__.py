"""Clase DatabaseStore - almacena conexión BD global."""

from infrastructure.repositories.database_store.set_database import SetDatabaseMixin
from infrastructure.repositories.database_store.get_database import GetDatabaseMixin


class DatabaseStore(SetDatabaseMixin, GetDatabaseMixin):
    """
    Almacenador centralizado de conexión a BD (Singleton).
    
    Combina:
        • SetDatabaseMixin - set_database()
        • GetDatabaseMixin - get_database()
    
    RESPONSABILIDAD: 1
    • Almacenar y recuperar la conexión a BD
    
    Patrón: Singleton para conexión global
    """
    
    _conn = None
    _db_path = None
    
    @classmethod
    def set_db_path(cls, db_path: str):
        """Guardar la ruta de la BD para reconexión"""
        cls._db_path = db_path
