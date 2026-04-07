"""
producto/
---------
Módulo de modelos de productos organizado por tipo.

Estructura:
    - __init__.py: Expone Producto y tipos concretos
    - contratos.py: TypedDicts (contratos de datos)
    - base.py: Clase abstracta Producto (propiedades, stock, validación)
    - simple.py: ProductoSimple
    - perecedero.py: ProductoPerecedero
    - digital.py: ProductoDigital
"""

from .base import Producto
from .contratos import ProductoSimpleData, ProductoPerecederoData, ProductoDigitalData
from .simple import ProductoSimple
from .perecedero import ProductoPerecedero
from .digital import ProductoDigital

__all__ = [
    'Producto',
    'ProductoSimple',
    'ProductoPerecedero',
    'ProductoDigital',
    'ProductoSimpleData',
    'ProductoPerecederoData',
    'ProductoDigitalData',
]
