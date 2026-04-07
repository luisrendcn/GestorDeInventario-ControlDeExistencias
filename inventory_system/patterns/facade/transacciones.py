"""
facade/transacciones.py
=======================
Mixin: Gestión de ventas y compras.

Responsabilidad:
    - Registrar ventas (reduce stock)
    - Registrar compras (aumenta stock)
    - Coordinar cambios de stock con transacciones
"""

from typing import Optional
from models import Transaccion


class TransaccionesMixin:
    """Mixin para operaciones de ventas y compras."""

    def registrar_venta(self, producto_id: str, cantidad: int) -> Transaccion:
        """
        Registra una venta: reduce stock del producto y crea transacción.
        Notifica a los observadores tras el cambio.
        """
        return self._inventario_service.registrar_venta(
            producto_id, cantidad, self._transaccion_service
        )

    def registrar_compra(
        self,
        producto_id: str,
        cantidad: int,
        precio_unitario: Optional[float] = None,
    ) -> Transaccion:
        """
        Registra una compra: aumenta stock del producto y crea transacción.
        Notifica a los observadores tras el cambio.
        """
        return self._inventario_service.registrar_compra(
            producto_id, cantidad, self._transaccion_service, precio_unitario
        )
