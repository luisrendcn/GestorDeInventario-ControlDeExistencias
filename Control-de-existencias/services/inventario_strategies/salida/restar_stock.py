"""
Operación aritmética: restar stock.
"""

from core.models import Producto


def restar_stock(producto: Producto, cantidad: int) -> None:
    """
    Restar cantidad del stock del producto.
    
    RESPONSABILIDAD ÚNICA: Aplicar la operación aritmética.
    """
    producto.reducir_stock(cantidad)
