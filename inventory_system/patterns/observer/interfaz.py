"""
observer/interfaz.py
====================
Interfaz abstracta del observador.

Responsabilidad:
    - Define contrato que deben cumplir todos los observadores
    - Asegura consistencia en el método de actualización
"""

from abc import ABC, abstractmethod
from models import Producto


class ObservadorStock(ABC):
    """Interfaz abstracta que deben implementar todos los observadores."""

    @abstractmethod
    def actualizar(self, producto: Producto, evento: str, cantidad: int) -> None:
        """
        Llamado cuando ocurre un evento de stock.

        Args:
            producto: El producto afectado.
            evento: Descripción del evento ('venta', 'compra', 'edicion').
            cantidad: Cantidad involucrada en el movimiento.
        """
        pass
