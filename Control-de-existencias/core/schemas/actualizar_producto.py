"""Schema para actualizar producto - combina estructura y validación."""

from core.schemas.actualizar_producto_dataclass import ActualizarProductoDataclassMixin
from core.schemas.validar_actualizar_producto import ValidarActualizarProductoMixin


class ActualizarProductoSchema(ActualizarProductoDataclassMixin, ValidarActualizarProductoMixin):
    """
    Schema para validar datos de actualización de producto.
    
    Combina:
        • ActualizarProductoDataclassMixin - Estructura de datos
        • ValidarActualizarProductoMixin - Método validar()
    
    RESPONSABILIDAD: 1
    • Validar que los campos opcionales sean correctos
    """
    pass
