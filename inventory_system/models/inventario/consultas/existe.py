"""
consultas/existe.py
===================
Operación: Verificar existencia de un producto.

Responsabilidad única:
    - Comprobar si un producto existe en el inventario por ID
"""


class ExisteMixin:
    """Mixin especializado en verificar existencia de productos."""

    def existe(self, id: str) -> bool:
        """
        Comprueba si existe un producto con ese ID en el inventario.
        
        Args:
            id: ID del producto a verificar
            
        Returns:
            True si existe, False en caso contrario
        """
        return id in self._productos
