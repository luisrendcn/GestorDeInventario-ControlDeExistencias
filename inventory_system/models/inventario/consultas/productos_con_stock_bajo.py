"""
consultas/productos_con_stock_bajo.py
======================================
Operación: Obtener productos con stock bajo.

Responsabilidad única:
    - Filtrar productos cuyo stock está por debajo del mínimo
"""

from typing import List


class ProductosConStockBajoMixin:
    """Mixin especializado en identificar productos con stock bajo."""

    def productos_con_stock_bajo(self) -> List['Producto']:
        """
        Retorna productos cuyo stock está por debajo del mínimo permitido.
        
        Útil para:
        - Alertas
        - Reordenes automáticas
        - Reportes de acción requerida
        
        Returns:
            Lista de productos con stock < stock_minimo
        """
        return [p for p in self._productos.values() if p.stock_bajo]
