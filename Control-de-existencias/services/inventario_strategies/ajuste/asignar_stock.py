"""
Operación: asignar valor exacto de stock.
"""

from core.models import Producto


def asignar_stock(producto: Producto, nuevo_stock: int) -> None:
    """
    Asignar valor exacto al stock del producto.
    
    RESPONSABILIDAD ÚNICA: Establecer valor exacto (no aritmética).
    """
    producto.establecer_stock(nuevo_stock)
