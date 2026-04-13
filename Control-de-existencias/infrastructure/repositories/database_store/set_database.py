"""
╔════════════════════════════════════════════════════════════════════════════╗
║   ARCHIVO: database_store/set_database.py                                 ║
║   RESPONSABILIDAD: Establecer conexión BD global                          ║
╚════════════════════════════════════════════════════════════════════════════╝

🎯 ÚNICA RESPONSABILIDAD:
   Almacenar la conexión BD en el singleton.
"""


class SetDatabaseMixin:
    """
    Mixin que agrega método para establecer conexión.
    
    RESPONSABILIDAD: 1
    • Guardar conexión BD en variable de clase
    
    Requiere:
        • _conn (class variable)
    """
    
    @classmethod
    def set_database(cls, conn):
        """
        Establecer la conexión BD global.
        
        Args:
            conn: Conexión SQLite a almacenar
        """
        cls._conn = conn
