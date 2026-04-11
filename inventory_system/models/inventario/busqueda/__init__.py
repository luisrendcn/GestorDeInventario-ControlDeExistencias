"""
busqueda/__init__.py
====================
Módulo de Búsqueda - Agrupa todas las operaciones de búsqueda.

Cada operación está en su propio archivo para máxima separación de responsabilidades.
El BúsquedaMixin combina todas ellas en una interfaz unificada.
"""

from .listar_todos import ListarTodosMixin
from .buscar_por_nombre import BuscarPorNombreMixin


class BúsquedaMixin(ListarTodosMixin, BuscarPorNombreMixin):
    """
    Mixin que agrupa todas las operaciones de búsqueda.
    
    Hereda de:
    - ListarTodosMixin: listar_todos()
    - BuscarPorNombreMixin: buscar_por_nombre()
    
    Propósito:
        Proporcionar interfaz unificada para búsquedas en inventario.
    """
    pass


__all__ = [
    'BúsquedaMixin',
    'ListarTodosMixin',
    'BuscarPorNombreMixin',
]
