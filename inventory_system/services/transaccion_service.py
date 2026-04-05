"""
services/transaccion_service.py
--------------------------------
Servicio de negocio para el registro y consulta de transacciones.

Aplica SRP: responsabilidad única de gestionar el historial de movimientos.
"""

from typing import List
from models.transaccion import Transaccion, TipoTransaccion
from models.producto import Producto
import uuid


class TransaccionService:
    """
    Gestiona el historial de ventas y compras.
    Crea transacciones y permite consultarlas.
    """

    def __init__(self):
        self._historial: List[Transaccion] = []

    def registrar(
        self,
        tipo: TipoTransaccion,
        producto: Producto,
        cantidad: int,
        precio_unitario: float,
    ) -> Transaccion:
        """
        Crea y almacena una nueva transacción.

        Args:
            tipo: VENTA o COMPRA.
            producto: Producto involucrado.
            cantidad: Unidades vendidas/compradas.
            precio_unitario: Precio por unidad en el momento de la transacción.

        Returns:
            La transacción creada.
        """
        transaccion = Transaccion(
            id=str(uuid.uuid4())[:8].upper(),
            tipo=tipo,
            producto_id=producto.id,
            producto_nombre=producto.nombre,
            cantidad=cantidad,
            precio_unitario=precio_unitario,
        )
        self._historial.append(transaccion)
        return transaccion

    def obtener_historial(self) -> List[Transaccion]:
        """Retorna el historial completo de transacciones."""
        return list(self._historial)

    def filtrar_por_tipo(self, tipo: TipoTransaccion) -> List[Transaccion]:
        """Retorna solo las transacciones del tipo especificado."""
        return [t for t in self._historial if t.tipo == tipo]

    def total_ingresos(self) -> float:
        """Calcula el total de ingresos por ventas."""
        return sum(t.total for t in self._historial if t.tipo == TipoTransaccion.VENTA)

    def total_costos(self) -> float:
        """Calcula el total de costos por compras."""
        return sum(t.total for t in self._historial if t.tipo == TipoTransaccion.COMPRA)
