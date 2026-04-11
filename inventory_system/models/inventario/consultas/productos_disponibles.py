"""
consultas/productos_disponibles.py
===================================
Operación: Obtener productos disponibles.

Responsabilidad única:
    - Filtrar productos con stock disponible (stock > 0)
"""

from typing import List


class ProductosDisponiblesMixin:
    """Mixin especializado en identificar productos disponibles."""

    def productos_disponibles(self) -> List['Producto']:
        """
        Retorna productos con stock disponible para venta o distribución.
        
        Útil para:
        - Decisiones de venta
        - Conocer artículos en stock
        - Reportes de disponibilidad
        
        Returns:
            Lista de productos con stock > 0
        """
        return [p for p in self._productos.values() if p.stock > 0]
