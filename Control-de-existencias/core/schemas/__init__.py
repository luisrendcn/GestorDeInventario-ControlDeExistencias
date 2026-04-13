"""Schemas de validación - punto de entrada centralizado."""

from core.schemas.crear_producto import CrearProductoSchema
from core.schemas.actualizar_producto import ActualizarProductoSchema
from core.schemas.movimiento import MovimientoSchema

__all__ = [
    'CrearProductoSchema',
    'ActualizarProductoSchema',
    'MovimientoSchema',
]
