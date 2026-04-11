"""
busqueda/listar_todos.py
=======================
Operación: Listar todos los productos del inventario.

Responsabilidad única:
    - Retornar una lista de todos los productos disponibles
"""

from typing import List


class ListarTodosMixin:
    """Mixin especializado en listar todos los productos."""

    def listar_todos(self) -> List['Producto']:
        """
        Retorna lista de todos los productos en el inventario.
        
        Returns:
            Lista con todos los productos almacenados
        """
        return list(self._productos.values())
