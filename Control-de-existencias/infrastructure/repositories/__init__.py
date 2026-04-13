"""Repositorios refactorizados - punto de entrada centralizado."""

from infrastructure.repositories.producto_repository import ProductoRepository
from infrastructure.repositories.movimiento_repository import MovimientoRepository
from infrastructure.repositories.database_store import DatabaseStore
from infrastructure.repositories.repositorio_factory import RepositorioFactory
from infrastructure.repositories.movimiento_repository_factory import MovimientoRepositoryFactory

__all__ = [
    'ProductoRepository',
    'MovimientoRepository',
    'DatabaseStore',
    'RepositorioFactory',
    'MovimientoRepositoryFactory',
]
