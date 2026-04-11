"""
consultas/__init__.py
=====================
Módulo Consultas - Agrupa todas las operaciones de consulta y análisis.

Cada operación está en su propio archivo para máxima separación de responsabilidades.
El ConsultasMixin combina todas ellas en una interfaz unificada.
"""

from .existe import ExisteMixin
from .total_productos import TotalProductosMixin
from .valor_total_inventario import ValorTotalInventarioMixin
from .productos_con_stock_bajo import ProductosConStockBajoMixin
from .productos_agotados import ProductosAgotadosMixin
from .productos_disponibles import ProductosDisponiblesMixin
from .obtener_stock_total import ObtenerStockTotalMixin
from .obtener_reporte_stock import ObtenerReporteStockMixin
from .obtener_productos_mayor_stock import ObtenerProductosMayorStockMixin
from .obtener_productos_menor_stock import ObtenerProductosMenorStockMixin


class ConsultasMixin(
    ExisteMixin,
    TotalProductosMixin,
    ValorTotalInventarioMixin,
    ProductosConStockBajoMixin,
    ProductosAgotadosMixin,
    ProductosDisponiblesMixin,
    ObtenerStockTotalMixin,
    ObtenerReporteStockMixin,
    ObtenerProductosMayorStockMixin,
    ObtenerProductosMenorStockMixin,
):
    """
    Mixin que agrupa todas las operaciones de consulta.
    
    Hereda de todas las operaciones especializadas para proporcionar
    consultas completas sobre el estado del inventario.
    
    Propósito:
        Análisis, reportes y consultas de existencias sin modificación de datos.
    """
    pass


__all__ = [
    'ConsultasMixin',
    'ExisteMixin',
    'TotalProductosMixin',
    'ValorTotalInventarioMixin',
    'ProductosConStockBajoMixin',
    'ProductosAgotadosMixin',
    'ProductosDisponiblesMixin',
    'ObtenerStockTotalMixin',
    'ObtenerReporteStockMixin',
    'ObtenerProductosMayorStockMixin',
    'ObtenerProductosMenorStockMixin',
]
