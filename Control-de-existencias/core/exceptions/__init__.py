"""Excepciones personalizadas del dominio - punto de entrada centralizado."""

from core.exceptions.inventario_error import InventarioError
from core.exceptions.producto_no_encontrado import ProductoNoEncontrado
from core.exceptions.stock_insuficiente import StockInsuficiente
from core.exceptions.datos_invalidos import DatosInvalidos
from core.exceptions.operacion_no_permitida import OperacionNoPermitida

__all__ = [
    'InventarioError',
    'ProductoNoEncontrado',
    'StockInsuficiente',
    'DatosInvalidos',
    'OperacionNoPermitida',
]
