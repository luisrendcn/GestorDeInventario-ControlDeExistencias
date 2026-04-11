"""
crud/eliminar.py
================
Operación: Eliminar un producto del inventario.

Responsabilidad única:
    - Remover producto del inventario
    - Registrar movimiento de eliminación
"""


class EliminarMixin:
    """Mixin especializado en eliminar productos."""

    def eliminar(self, id: str) -> 'Producto':
        """
        Elimina un producto del inventario y lo retorna.
        
        Valida que el producto exista antes de eliminarlo.
        Registra la eliminación en el historial de movimientos.
        
        Args:
            id: ID del producto a eliminar
            
        Returns:
            Producto eliminado
            
        Raises:
            ValueError: Si el producto no existe
        """
        if id not in self._productos:
            raise ValueError(f"Producto con ID '{id}' no encontrado.")
        
        producto = self._productos.pop(id)
        self.registrar_movimiento(id, 'eliminacion', producto.stock)
        
        return producto
