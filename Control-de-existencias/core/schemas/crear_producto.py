"""Schema para crear producto - combina estructura y validación."""

from core.schemas.crear_producto_dataclass import CrearProductoDataclassMixin
from core.schemas.validar_crear_producto import ValidarCrearProductoMixin


class CrearProductoSchema(CrearProductoDataclassMixin, ValidarCrearProductoMixin):
    """
    Schema para validar datos de creación de producto.
    
    Combina:
        • CrearProductoDataclassMixin - Estructura de datos
        • ValidarCrearProductoMixin - Método validar()
    
    RESPONSABILIDAD: 1
    • Validar que todos los campos requeridos sean correctos
    """
    pass
