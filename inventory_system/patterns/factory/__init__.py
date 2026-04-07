"""
factory/
--------
Patrón creacional: Factory Method (Método de Fábrica).

Sistema de creación de productos con Template Method y registry inmutable.

Componentes:
    - ProductoFactory: clase base abstracta (Template Method)
    - ProductoSimpleFactory, ProductoPerecederoFactory, ProductoDigitalFactory: fábricas concretas
    - FactoryRegistry: registro con inyección de dependencias
    - FactoryManager: interfaz global para compatibilidad
"""

from .bases import ProductoFactory
from .concretas import (
    ProductoSimpleFactory,
    ProductoPerecederoFactory,
    ProductoDigitalFactory,
)
from .registry import FactoryRegistry
from .factory import FactoryManager, obtener_fabrica, crear_producto, tipos_disponibles

__all__ = [
    'ProductoFactory',
    'ProductoSimpleFactory',
    'ProductoPerecederoFactory',
    'ProductoDigitalFactory',
    'FactoryRegistry',
    'FactoryManager',
    'obtener_fabrica',
    'crear_producto',
    'tipos_disponibles',
]
