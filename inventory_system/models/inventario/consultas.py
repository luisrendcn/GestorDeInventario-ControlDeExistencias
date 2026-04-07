"""
inventario/consultas.py
=======================
Mixin que maneja consultas y estadísticas del inventario.
"""

from typing import List


class ConsultasMixin:
    """Mixin para consultas, filtros y estadísticas."""

    def existe(self, id: str) -> bool:
        """Comprueba si existe un producto con ese ID."""
        return id in self._productos

    def total_productos(self) -> int:
        """Número total de productos en el inventario."""
        return len(self._productos)

    def valor_total_inventario(self) -> float:
        """Calcula el valor total del inventario (precio × stock)."""
        return sum(p.precio * p.stock for p in self._productos.values())

    def productos_con_stock_bajo(self) -> List[Producto]:
        """Retorna productos cuyo stock está por debajo del mínimo."""
        return [p for p in self._productos.values() if p.stock_bajo]
