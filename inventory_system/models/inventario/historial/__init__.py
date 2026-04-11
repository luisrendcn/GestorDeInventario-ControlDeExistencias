"""
historial/__init__.py
=====================
Módulo Historial - Agrupa todas las operaciones de auditoría de movimientos.

Responsabilidad:
    - Gestionar registro de auditoría
    - Consultar historial de cambios
    - Limpiar registros
"""

from .registrar_movimiento import RegistrarMovimientoMixin
from .obtener_historial import ObtenerHistorialMixin
from .limpiar_historial import LimpiarHistorialMixin


class HistorialMixin(
    RegistrarMovimientoMixin,
    ObtenerHistorialMixin,
    LimpiarHistorialMixin,
):
    """
    Mixin que agrupa todas las operaciones de auditoría e historial.
    
    Responsabilidad única:
        Mantener y consultar el historial de movimientos de stock.
    
    Hereda de:
    - RegistrarMovimientoMixin: registrar_movimiento()
    - ObtenerHistorialMixin: obtener_historial()
    - LimpiarHistorialMixin: limpiar_historial()
    """
    pass


__all__ = [
    'HistorialMixin',
    'RegistrarMovimientoMixin',
    'ObtenerHistorialMixin',
    'LimpiarHistorialMixin',
]
