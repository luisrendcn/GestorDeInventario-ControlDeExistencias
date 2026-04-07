"""
producto/contratos.py
=====================
TypedDicts que documentan los contratos de datos para crear productos.

Estas clases NO tienen lógica, solo especifican qué campos se esperan.
Proporcionan type hints para IDE y type checking con mypy.
"""

from typing import TypedDict, NotRequired


class ProductoSimpleData(TypedDict):
    """Contrato: campos esperados para crear ProductoSimple."""
    id: str
    nombre: str
    precio: float
    stock: int
    stock_minimo: NotRequired[int]
    categoria: NotRequired[str]


class ProductoPerecederoData(TypedDict):
    """Contrato: campos esperados para crear ProductoPerecedero."""
    id: str
    nombre: str
    precio: float
    stock: int
    fecha_vencimiento: str  # Formato ISO: YYYY-MM-DD
    stock_minimo: NotRequired[int]


class ProductoDigitalData(TypedDict):
    """Contrato: campos esperados para crear ProductoDigital."""
    id: str
    nombre: str
    precio: float
    stock: int
    url_descarga: NotRequired[str]
    stock_minimo: NotRequired[int]
