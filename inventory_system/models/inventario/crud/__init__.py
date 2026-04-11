"""
crud/__init__.py
================
Módulo CRUD - Agrupa todas las operaciones de creación, lectura, actualización y eliminación.

Cada operación está en su propio archivo para máxima separación de responsabilidades.
El CRUDMixin combina todas ellas en una interfaz unificada.
"""

from .agregar import AgregarMixin
from .obtener import ObtenerMixin
from .obtener_o_error import ObtenerOErrorMixin
from .eliminar import EliminarMixin
from .actualizar_stock_entrada import ActualizarStockEntradaMixin
from .actualizar_stock_salida import ActualizarStockSalidaMixin
from .obtener_stock_actual import ObtenerStockActualMixin
from .validar_stock_no_negativo import ValidarStockNoNegativoMixin


class CRUDMixin(
    AgregarMixin,
    ObtenerMixin,
    ObtenerOErrorMixin,
    EliminarMixin,
    ActualizarStockEntradaMixin,
    ActualizarStockSalidaMixin,
    ObtenerStockActualMixin,
    ValidarStockNoNegativoMixin,
):
    """
    Mixin que agrupa todas las operaciones CRUD.
    
    Hereda de todas las operaciones especializadas:
    - AgregarMixin: agregar()
    - ObtenerMixin: obtener()
    - ObtenerOErrorMixin: obtener_o_error()
    - EliminarMixin: eliminar()
    - ActualizarStockEntradaMixin: actualizar_stock_entrada()
    - ActualizarStockSalidaMixin: actualizar_stock_salida()
    - ObtenerStockActualMixin: obtener_stock_actual()
    - ValidarStockNoNegativoMixin: validar_stock_no_negativo()
    
    Propósito:
        Proporcionar operaciones completas de CRUD con control de existencias.
    """
    pass


__all__ = [
    'CRUDMixin',
    'AgregarMixin',
    'ObtenerMixin',
    'ObtenerOErrorMixin',
    'EliminarMixin',
    'ActualizarStockEntradaMixin',
    'ActualizarStockSalidaMixin',
    'ObtenerStockActualMixin',
    'ValidarStockNoNegativoMixin',
]
