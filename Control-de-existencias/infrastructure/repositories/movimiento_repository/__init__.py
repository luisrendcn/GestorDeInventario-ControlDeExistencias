"""Clase MovimientoRepository - combina historial de movimientos."""

from infrastructure.repositories.movimiento_repository.registrar_movimiento import RegistrarMovimientoMixin
from infrastructure.repositories.movimiento_repository.obtener_historial import ObtenerHistorialMixin
from infrastructure.repositories.movimiento_repository.limpiar_historial import LimpiarHistorialMixin
from infrastructure.database import QueryExecutor, QueryReader


class MovimientoRepository(RegistrarMovimientoMixin, ObtenerHistorialMixin, LimpiarHistorialMixin):
    """
    Repositorio para historial de movimientos de stock.
    
    Combina:
        • RegistrarMovimientoMixin - registrar_movimiento()
        • ObtenerHistorialMixin - obtener_historial()
        • LimpiarHistorialMixin - limpiar_historial()
    
    RESPONSABILIDAD: 1
    • Gestionar historial de movimientos de stock
    
    INYECCIÓN DE DEPENDENCIAS:
        • conn (sqlite3.Connection): Conexión inyectada
    
    INTERNAMENTE USA:
        • QueryExecutor: Para INSERT, DELETE
        • QueryReader: Para SELECT
    """
    
    def __init__(self, conn):
        """
        Inicializar con inyección de dependencias.
        
        Args:
            conn: Conexión SQLite ya configurada
        """
        self.conn = conn
        self.executor = QueryExecutor(conn)
        self.reader = QueryReader(conn)
