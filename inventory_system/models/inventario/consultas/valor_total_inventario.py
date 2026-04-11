"""
consultas/valor_total_inventario.py
====================================
Operación: Calcular valor total del inventario.

Responsabilidad única:
    - Sumar precio × stock de todos los productos
"""


class ValorTotalInventarioMixin:
    """Mixin especializado en calcular valor total del inventario."""

    def valor_total_inventario(self) -> float:
        """
        Calcula el valor monetario total del inventario (precio × stock).
        
        Returns:
            Valor total en moneda (suma de precio * stock de todos los productos)
        """
        return sum(p.precio * p.stock for p in self._productos.values())
