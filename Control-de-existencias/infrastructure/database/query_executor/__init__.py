"""Clase QueryExecutor - ejecuta queries de modificación."""

from infrastructure.database.query_executor.ejecutar import EjecutarMixin


class QueryExecutor(EjecutarMixin):
    """
    Ejecutar queries de MODIFICACIÓN (INSERT, UPDATE, DELETE).
    
    Combina:
        • EjecutarMixin - ejecutar()
    
    RESPONSABILIDAD: 1
    • Ejecutar queries que CAMBIAN datos
    """
    
    def __init__(self, conn):
        """
        Inicializar con conexión existente.
        
        Args:
            conn: Conexión SQLite (de ConnectionManager)
        """
        self.conn = conn
