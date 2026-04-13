"""
╔════════════════════════════════════════════════════════════════════════════╗
║        ARCHIVO: core/schemas/validar_actualizar_producto.py               ║
║        RESPONSABILIDAD: Validar datos de actualización de producto        ║
╚════════════════════════════════════════════════════════════════════════════╝

🎯 ÚNICA RESPONSABILIDAD:
   Validar que los campos opcionales de actualización sean válidos.
   
💡 VALIDACIONES (solo para campos presentes):
   • Nombre no vacío (si existe)
   • Precio >= 0 (si existe)
   • Stock mínimo >= 0 (si existe)
"""

from core.exceptions import DatosInvalidos


class ValidarActualizarProductoMixin:
    """
    Mixin que agrega validación a ActualizarProductoSchema.
    
    RESPONSABILIDAD: 1
    • Validar campos opcionales de actualización
    
    Requiere atributos:
        • self.nombre, precio, stock_minimo (todos Optional)
    """
    
    def validar(self):
        """
        Validar datos de actualización de producto.
        
        Solo valida campos que están presentes (no None)
        """
        if self.nombre is not None and not self.nombre.strip():
            raise DatosInvalidos("Nombre no puede estar vacío")
        
        if self.precio is not None and self.precio < 0:
            raise DatosInvalidos("Precio no puede ser negativo")
        
        if self.stock_minimo is not None and self.stock_minimo < 0:
            raise DatosInvalidos("Stock mínimo no puede ser negativo")
