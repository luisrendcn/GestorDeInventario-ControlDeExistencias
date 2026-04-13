"""Clase ConnectionManager - combina conectar y desconectar."""

from infrastructure.database.connection_manager.conectar import ConectarMixin
from infrastructure.database.connection_manager.desconectar import DesconectarMixin


class ConnectionManager(ConectarMixin, DesconectarMixin):
    """
    Gestionar el CICLO DE VIDA de la conexión SQLite.
    
    Combina:
        • ConectarMixin - conectar()
        • DesconectarMixin - desconectar(), cerrar()
    
    RESPONSABILIDAD: 1
    • Conectar/desconectar de la BD
    """
    
    def __init__(self, db_path: str = "control_existencias.db"):
        """
        Inicializar manager (sin conectar yet).
        
        Args:
            db_path: Ruta al archivo SQLite
        """
        self.db_path = db_path
        self.conn = None
