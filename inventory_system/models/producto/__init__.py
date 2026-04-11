"""
models/producto/__init__.py
============================
Orquestador: Producto compone todos los mixins mediante herencia.

Estructura de responsabilidades:
┌─ ValidacionesMixin ──────────► __post_init__
├─ PropiedadesMixin ───────────► stock_bajo, agotado, valor_total
├─ StockMixin ─────────────────► agregar_stock, reducir_stock, ajustar_stock
└─ SerializacionMixin ─────────► to_dict

Cada mixin: una responsabilidad única
Producto: solo orquesta
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from .validaciones import ValidacionesMixin
from .propiedades import PropiedadesMixin
from .stock import StockMixin
from .serializacion import SerializacionMixin


@dataclass
class Producto(
    ValidacionesMixin,
    PropiedadesMixin,
    StockMixin,
    SerializacionMixin,
):
    """Modelo genérico de Producto para Control de Existencias."""
    
    id: str
    nombre: str
    precio: float
    stock: int
    stock_minimo: int = 5
    descripcion: Optional[str] = None
    fecha_creacion: datetime = field(default_factory=datetime.now)


__all__ = ["Producto"]
