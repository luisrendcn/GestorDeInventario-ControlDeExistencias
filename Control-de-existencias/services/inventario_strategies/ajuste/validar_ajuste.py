"""
Validación de datos de ajuste.
"""

from core.exceptions import DatosInvalidos


def validar_ajuste(nuevo_stock: int) -> None:
    """Validar que nuevo_stock es válido para ajuste."""
    if nuevo_stock < 0:
        raise DatosInvalidos("El stock no puede ser negativo")
