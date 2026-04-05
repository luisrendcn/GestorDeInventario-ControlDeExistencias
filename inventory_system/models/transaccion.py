"""
models/transaccion.py
---------------------
Clases de dominio para registrar compras y ventas (historial de movimientos).

Aplica encapsulamiento e inmutabilidad conceptual:
las transacciones no deben modificarse una vez registradas.
"""

from datetime import datetime
from enum import Enum


class TipoTransaccion(Enum):
    COMPRA = "Compra"
    VENTA = "Venta"


class Transaccion:
    """
    Representa un movimiento de stock (compra o venta).
    Inmutable por convención: no expone setters.
    """

    def __init__(
        self,
        id: str,
        tipo: TipoTransaccion,
        producto_id: str,
        producto_nombre: str,
        cantidad: int,
        precio_unitario: float,
    ):
        self._id = id
        self._tipo = tipo
        self._producto_id = producto_id
        self._producto_nombre = producto_nombre
        self._cantidad = cantidad
        self._precio_unitario = precio_unitario
        self._fecha = datetime.now()

    @property
    def id(self) -> str:
        return self._id

    @property
    def tipo(self) -> TipoTransaccion:
        return self._tipo

    @property
    def producto_id(self) -> str:
        return self._producto_id

    @property
    def producto_nombre(self) -> str:
        return self._producto_nombre

    @property
    def cantidad(self) -> int:
        return self._cantidad

    @property
    def precio_unitario(self) -> float:
        return self._precio_unitario

    @property
    def total(self) -> float:
        return self._cantidad * self._precio_unitario

    @property
    def fecha(self) -> datetime:
        return self._fecha

    def __repr__(self) -> str:
        return (
            f"[{self._tipo.value}] {self._fecha.strftime('%Y-%m-%d %H:%M')} | "
            f"ID: {self._id} | {self._producto_nombre} x{self._cantidad} "
            f"@ ${self._precio_unitario:.2f} = ${self.total:.2f}"
        )
