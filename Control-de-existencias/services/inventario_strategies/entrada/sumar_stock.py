"""
Operación aritmética: sumar stock.
"""

from core.models import Producto


def sumar_stock(producto: Producto, cantidad: int) -> None:
    """
    Sumar cantidad al stock del producto.
    
    RESPONSABILIDAD ÚNICA: Aplicar la operación aritmética.
    """
    producto.agregar_stock(cantidad)
