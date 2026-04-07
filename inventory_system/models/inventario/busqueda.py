"""
inventario/busqueda.py
======================
Mixin que maneja búsqueda y listado de productos.
"""

from typing import List


class BúsquedaMixin:
    """Mixin para búsqueda y listado de productos."""

    def listar_todos(self) -> List[Producto]:
        """Retorna lista de todos los productos."""
        return list(self._productos.values())

    def buscar_por_nombre(self, nombre: str) -> List[Producto]:
        """Búsqueda parcial por nombre (case-insensitive)."""
        termino = nombre.lower()
        return [p for p in self._productos.values() if termino in p.nombre.lower()]
