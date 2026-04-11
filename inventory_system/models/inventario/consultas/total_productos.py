"""
consultas/total_productos.py
=============================
Operación: Obtener cantidad total de productos.

Responsabilidad única:
    - Contar productos únicos en el inventario
"""


class TotalProductosMixin:
    """Mixin especializado en contar productos."""

    def total_productos(self) -> int:
        """
        Retorna el número total de productos en el inventario.
        
        Returns:
            Cantidad de productos únicos (registros)
        """
        return len(self._productos)
