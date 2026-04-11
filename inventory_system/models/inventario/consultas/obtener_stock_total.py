"""
consultas/obtener_stock_total.py
=================================
Operación: Obtener cantidad total de unidades.

Responsabilidad única:
    - Sumar stock de todos los productos
"""


class ObtenerStockTotalMixin:
    """Mixin especializado en obtener stock total."""

    def obtener_stock_total(self) -> int:
        """
        Obtiene la cantidad total de unidades en stock (suma de todos los productos).
        
        Returns:
            Suma total de unidades en inventario
        """
        return sum(p.stock for p in self._productos.values())
