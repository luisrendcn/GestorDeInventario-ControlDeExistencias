"""
historial/registrar_movimiento.py
==================================
Operación: Registrar movimiento de stock.

Responsabilidad única:
    - Crear un registro de auditoría de movimiento
    - Almacenar timestamp, tipo, cantidad
"""

from datetime import datetime
from typing import Dict


class RegistrarMovimientoMixin:
    """Mixin especializado en registrar movimientos de stock."""

    def registrar_movimiento(self, producto_id: str, tipo: str, cantidad: int) -> None:
        """
        Registra un movimiento de stock en el historial de auditoría.
        
        Crea un registro con timestamp automático para cada movimiento
        (entrada, salida, eliminación, etc).
        
        Args:
            producto_id: ID del producto
            tipo: Tipo de movimiento ('entrada', 'salida', 'eliminacion', etc)
            cantidad: Cantidad movida
        """
        movimiento = {
            'timestamp': datetime.now(),
            'producto_id': producto_id,
            'tipo': tipo,
            'cantidad': cantidad
        }
        self._historial_movimientos.append(movimiento)
