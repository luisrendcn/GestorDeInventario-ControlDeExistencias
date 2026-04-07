"""
transaccion/
-----------
Módulo de modelos de transacciones (compras y ventas).

Estructura:
    - __init__.py: Expone Transaccion y TipoTransaccion
    - tipos.py: Enum TipoTransaccion
    - transaccion.py: Clase Transaccion
"""

from .tipos import TipoTransaccion
from .transaccion import Transaccion

__all__ = ['Transaccion', 'TipoTransaccion']
