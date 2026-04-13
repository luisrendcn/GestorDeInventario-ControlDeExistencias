"""
Validación de datos de salida.
"""

from core.schemas import MovimientoSchema
from core.exceptions import DatosInvalidos, StockInsuficiente
from core.models import Producto


def validar_salida(cantidad: int) -> None:
    """Validar que cantidad es válida para salida."""
    if cantidad <= 0:
        raise DatosInvalidos("La cantidad debe ser positiva")


def validar_disponibilidad(producto: Producto, cantidad: int) -> None:
    """
    Validar que hay suficiente stock.
    
    DIFERENCIA CLAVE con ENTRADA: SALIDA valida disponibilidad.
    """
    if cantidad > producto.stock:
        raise StockInsuficiente(
            f"Stock insuficiente: disponible {producto.stock}, "
            f"solicitado {cantidad}"
        )


def validar_schema(producto_id: str, cantidad: int, motivo: str = 'Salida') -> None:
    """Validar esquema de movimiento."""
    schema = MovimientoSchema(
        producto_id=producto_id,
        cantidad=cantidad,
        motivo=motivo or 'Salida'
    )
    schema.validar()
