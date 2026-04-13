"""Clase RepositorioFactory - factory para ProductoRepository."""

from infrastructure.repositories.repositorio_factory.get_producto_repository import GetProductoRepositoryMixin


class RepositorioFactory(GetProductoRepositoryMixin):
    """
    Factory para crear repositorio de productos.
    
    Combina:
        • GetProductoRepositoryMixin - get_producto_repository()
    
    Implementa el FACTORY METHOD PATTERN:
        • Evita múltiples instancias
        • Centraliza creación
        • Lazy initialization + Singleton
    
    RESPONSABILIDAD: 1
    • Crear y retornar ProductoRepository singleton
    
    PRECONDICIÓN: DatabaseStore.set_database() debe llamarse antes
    """
    
    _producto_repo = None
