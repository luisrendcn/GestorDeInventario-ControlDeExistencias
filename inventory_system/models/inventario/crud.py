"""
inventario/crud.py
==================
Mixin que maneja operaciones CRUD básicas del inventario.
"""

from typing import Optional


class CRUDMixin:
    """Mixin para operaciones CRUD en el inventario."""

    def agregar(self, producto: Producto) -> None:
        """Agrega un nuevo producto. Lanza error si el ID ya existe."""
        if producto.id in self._productos:
            raise ValueError(f"Ya existe un producto con ID '{producto.id}'.")
        self._productos[producto.id] = producto

    def obtener(self, id: str) -> Optional[Producto]:
        """Retorna el producto por ID, o None si no existe."""
        return self._productos.get(id)

    def obtener_o_error(self, id: str) -> Producto:
        """Retorna el producto por ID. Lanza ValueError si no existe."""
        producto = self.obtener(id)
        if producto is None:
            raise ValueError(f"Producto con ID '{id}' no encontrado.")
        return producto

    def eliminar(self, id: str) -> Producto:
        """Elimina y retorna el producto. Lanza error si no existe."""
        if id not in self._productos:
            raise ValueError(f"Producto con ID '{id}' no encontrado.")
        return self._productos.pop(id)
