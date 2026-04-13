"""Clase MovimientoRepositoryFactory - factory para MovimientoRepository."""

from infrastructure.repositories.movimiento_repository_factory.get_movimiento_repository import GetMovimientoRepositoryMixin


class MovimientoRepositoryFactory(GetMovimientoRepositoryMixin):
    """
    Factory para crear repositorio de movimientos.
    
    Combina:
        • GetMovimientoRepositoryMixin - get_movimiento_repository()
    
    Implementa el FACTORY METHOD PATTERN:
        • Evita múltiples instancias
        • Centraliza creación
        • Lazy initialization + Singleton
    
    RESPONSABILIDAD: 1
    • Crear y retornar MovimientoRepository singleton
    
    PRECONDICIÓN: DatabaseStore.set_database() debe llamarse antes
    """
    
    _movimiento_repo = None
