"""
producto/validaciones.py
========================
Responsabilidad única: Validar datos del producto al crearlo.
"""


class ValidacionesMixin:
    """Mixin especializado en validaciones de producto."""
    
    def __post_init__(self):
        """Validaciones al crear producto."""
        if not self.id or not self.nombre:
            raise ValueError("ID y nombre son requeridos")
        if self.precio < 0:
            raise ValueError("Precio no puede ser negativo")
        if self.stock < 0:
            raise ValueError("Stock no puede ser negativo")
        if self.stock_minimo < 0:
            raise ValueError("Stock mínimo no puede ser negativo")
