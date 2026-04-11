"""
consultas/obtener_productos_menor_stock.py
============================================
Operación: Obtener productos con menos stock.

Responsabilidad única:
    - Ranking de productos por cantidad de stock (ascendente)
"""

from typing import List


class ObtenerProductosMenorStockMixin:
    """Mixin especializado en ranking de productos por stock ascendente."""

    def obtener_productos_menor_stock(self, limite: int = 5) -> List['Producto']:
        """
        Retorna los productos con menor cantidad de stock.
        
        Útil para:
        - Identificar candidatos a reorden
        - Prevenir agotamientos
        - Visibilidad de niveles críticos
        
        Args:
            limite: Número máximo de productos a retornar (default: 5)
            
        Returns:
            Lista de productos ordenados por stock ascendente
        """
        return sorted(
            self._productos.values(),
            key=lambda p: p.stock
        )[:limite]
