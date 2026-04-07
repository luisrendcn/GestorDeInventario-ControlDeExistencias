"""
transaccion/tipos.py
====================
Enumeración de tipos de transacción.
"""

from enum import Enum


class TipoTransaccion(Enum):
    """Tipos de transacciones posibles en el inventario."""
    COMPRA = "Compra"
    VENTA = "Venta"
