"""
╔════════════════════════════════════════════════════════════════════════════╗
║          ARCHIVO: core/schemas/validar_crear_producto.py                  ║
║          RESPONSABILIDAD: Validar datos de creación de producto           ║
╚════════════════════════════════════════════════════════════════════════════╝

🎯 ÚNICA RESPONSABILIDAD:
   Validar que todos los campos para crear producto sean válidos.
   
💡 VALIDACIONES:
   • ID no vacío
   • Nombre no vacío
   • Precio >= 0
   • Stock >= 0
   • Stock mínimo >= 0
"""

from core.exceptions import DatosInvalidos


class ValidarCrearProductoMixin:
    """
    Mixin que agrega validación a CrearProductoSchema.
    
    RESPONSABILIDAD: 1
    • Validar todos los campos requeridos para crear producto
    
    Requiere atributos:
        • self.id, nombre, precio, stock, stock_minimo
    """
    
    def validar(self):
        """
        Validar datos de creación de producto.
        
        Lanza DatosInvalidos si algún campo es inválido
        """
        if not self.id or not self.id.strip():
            raise DatosInvalidos("ID del producto es requerido")
        
        if not self.nombre or not self.nombre.strip():
            raise DatosInvalidos("Nombre del producto es requerido")
        
        if self.precio < 0:
            raise DatosInvalidos("Precio no puede ser negativo")
        
        if self.stock < 0:
            raise DatosInvalidos("Stock no puede ser negativo")
        
        if self.stock_minimo < 0:
            raise DatosInvalidos("Stock mínimo no puede ser negativo")
