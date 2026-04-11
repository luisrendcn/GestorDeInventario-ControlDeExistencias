"""
consultas/productos_agotados.py
================================
Operación: Obtener productos agotados.

Responsabilidad única:
    - Filtrar productos sin stock (stock = 0)
"""

from typing import List


class ProductosAgotadosMixin:
    """Mixin especializado en identificar productos agotados."""

    def productos_agotados(self) -> List['Producto']:
        """
        Retorna productos sin stock (stock = 0).
        
        Útil para:
        - Alertas de agotamiento
        - Reportes críticos
        - Gestión de reposición urgente
        
        Returns:
            Lista de productos con stock == 0
        """
        return [p for p in self._productos.values() if p.stock == 0]
