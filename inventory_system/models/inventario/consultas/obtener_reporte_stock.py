"""
consultas/obtener_reporte_stock.py
===================================
Operación: Generar reporte completo de stock.

Responsabilidad única:
    - Compilar estadísticas globales del inventario
"""

from typing import Dict


class ObtenerReporteStockMixin:
    """Mixin especializado en generar reportes completos."""

    def obtener_reporte_stock(self) -> Dict:
        """
        Genera un reporte completo del estado del inventario.
        
        Incluye:
        - Totalización de productos y unidades
        - Valor total del inventario
        - Estadísticas de disponibilidad
        - Promedios
        
        Returns:
            Diccionario con estadísticas completas
        """
        productos_todos = list(self._productos.values())
        
        return {
            'total_productos': self.total_productos(),
            'total_unidades': self.obtener_stock_total(),
            'valor_total': self.valor_total_inventario(),
            'productos_disponibles': len(self.productos_disponibles()),
            'productos_agotados': len(self.productos_agotados()),
            'productos_stock_bajo': len(self.productos_con_stock_bajo()),
            'stock_promedio': (
                self.obtener_stock_total() / self.total_productos() 
                if self.total_productos() > 0 else 0
            ),
            'precio_promedio': (
                sum(p.precio for p in productos_todos) / len(productos_todos)
                if productos_todos else 0
            ),
            'valor_promedio_producto': (
                self.valor_total_inventario() / self.total_productos()
                if self.total_productos() > 0 else 0
            )
        }
