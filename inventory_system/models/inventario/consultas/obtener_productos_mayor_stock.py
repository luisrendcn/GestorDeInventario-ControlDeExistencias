"""
consultas/obtener_productos_mayor_stock.py
============================================
Operación: Obtener productos con más stock.

Responsabilidad única:
    - Ranking de productos por cantidad de stock (descendente)
"""

from typing import List


class ObtenerProductosMayorStockMixin:
    """Mixin especializado en ranking de productos por stock descendente."""

    def obtener_productos_mayor_stock(self, limite: int = 5) -> List['Producto']:
        """
        Retorna los productos con mayor cantidad de stock.
        
        Útil para:
        - Identificar productos con exceso de stock
        - Análisis de almacenamiento
        - Decisiones de promoción
        
        Args:
            limite: Número máximo de productos a retornar (default: 5)
            
        Returns:
            Lista de productos ordenados por stock descendente
        """
        return sorted(
            self._productos.values(),
            key=lambda p: p.stock,
            reverse=True
        )[:limite]
