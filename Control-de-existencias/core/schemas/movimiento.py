"""Schema para movimiento - combina estructura y validación."""

from core.schemas.movimiento_dataclass import MovimientoDataclassMixin
from core.schemas.validar_movimiento import ValidarMovimientoMixin


class MovimientoSchema(MovimientoDataclassMixin, ValidarMovimientoMixin):
    """
    Schema para validar datos de movimiento de stock.
    
    Combina:
        • MovimientoDataclassMixin - Estructura de datos
        • ValidarMovimientoMixin - Método validar()
    
    RESPONSABILIDAD: 1
    • Validar que los datos del movimiento sean correctos
    """
    pass
