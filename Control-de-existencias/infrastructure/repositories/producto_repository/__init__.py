"""Clase ProductoRepository - combina CRUD de productos."""

from infrastructure.repositories.producto_repository.crear import CrearMixin
from infrastructure.repositories.producto_repository.obtener import ObtenerMixin
from infrastructure.repositories.producto_repository.listar import ListarMixin
from infrastructure.repositories.producto_repository.eliminar import EliminarMixin
from infrastructure.repositories.producto_repository.actualizar import ActualizarMixin
from infrastructure.database import QueryExecutor, QueryReader


class ProductoRepository(CrearMixin, ObtenerMixin, ListarMixin, EliminarMixin, ActualizarMixin):
    """
    Repositorio de acceso a datos para Productos.
    
    Combina:
        • CrearMixin - crear()
        • ObtenerMixin - obtener()
        • ListarMixin - listar()
        • EliminarMixin - eliminar()
        • ActualizarMixin - actualizar()
    
    RESPONSABILIDAD: 1
    • Gestionar operaciones CRUD de Productos
    
    INYECCIÓN DE DEPENDENCIAS:
        • conn (sqlite3.Connection): Conexión inyectada
    
    INTERNAMENTE USA:
        • QueryExecutor: Para INSERT, UPDATE, DELETE
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
