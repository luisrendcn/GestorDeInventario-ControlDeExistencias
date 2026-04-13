"""Clase DatabaseCleaner - limpia la base de datos."""

from infrastructure.database.database_cleaner.limpiar_base_datos import LimpiarBaseDatosMixin


class DatabaseCleaner(LimpiarBaseDatosMixin):
    """
    Limpiar/RESETEAR BD (para desarrollo y testing).
    
    Combina:
        • LimpiarBaseDatosMixin - limpiar_base_datos()
    
    RESPONSABILIDAD: 1
    • Limpiar toda la BD (IRREVERSIBLE)
    """
    
    def __init__(self, conn):
        """
        Inicializar con conexión existente.
        
        Args:
            conn: Conexión SQLite (de ConnectionManager)
        """
        self.conn = conn
