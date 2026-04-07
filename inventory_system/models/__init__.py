"""
models/
-------
Módulo de modelos de dominio de la aplicación.

Contiene:
    - Producto: Clase base de productos
    - ProductoSimple, ProductoPerecedero, ProductoDigital: Tipos concretos
    - Transaccion: Registro de movimientos de inventario
    - Inventario: Repositorio de productos organizado con mixins
"""

from .producto import (
    Producto,
    ProductoSimple,
    ProductoPerecedero,
    ProductoDigital,
    ProductoSimpleData,
    ProductoPerecederoData,
    ProductoDigitalData,
)
from .transaccion import Transaccion, TipoTransaccion
from .inventario import Inventario

__all__ = [
    'Producto',
    'ProductoSimple',
    'ProductoPerecedero',
    'ProductoDigital',
    'ProductoSimpleData',
    'ProductoPerecederoData',
    'ProductoDigitalData',
    'Transaccion',
    'TipoTransaccion',
    'Inventario',
]
