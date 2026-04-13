"""
Validación de datos de entrada.
"""

from core.schemas import MovimientoSchema
from core.exceptions import DatosInvalidos


def validar_entrada(cantidad: int) -> None:
    """Validar que cantidad es válida para entrada."""
    if cantidad <= 0:
        raise DatosInvalidos("La cantidad debe ser positiva")


def validar_schema(producto_id: str, cantidad: int, motivo: str = 'Entrada') -> None:
    """Validar esquema de movimiento."""
    schema = MovimientoSchema(
        producto_id=producto_id,
        cantidad=cantidad,
        motivo=motivo or 'Entrada'
    )
    schema.validar()
