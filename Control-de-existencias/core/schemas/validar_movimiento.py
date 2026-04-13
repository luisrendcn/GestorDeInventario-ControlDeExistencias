"""
╔════════════════════════════════════════════════════════════════════════════╗
║            ARCHIVO: core/schemas/validar_movimiento.py                    ║
║            RESPONSABILIDAD: Validar datos de movimiento                   ║
╚════════════════════════════════════════════════════════════════════════════╝

🎯 ÚNICA RESPONSABILIDAD:
   Validar que los datos del movimiento sean correctos.
   
💡 VALIDACIONES:
   • producto_id no vacío
   • cantidad > 0
"""

from core.exceptions import DatosInvalidos


class ValidarMovimientoMixin:
    """
    Mixin que agrega validación a MovimientoSchema.
    
    RESPONSABILIDAD: 1
    • Validar datos de movimiento de stock
    
    Requiere atributos:
        • self.producto_id, cantidad
    """
    
    def validar(self):
        """
        Validar datos de movimiento.
        
        Lanza DatosInvalidos si algún campo es inválido
        """
        if not self.producto_id or not self.producto_id.strip():
            raise DatosInvalidos("ID del producto es requerido")
        
        if self.cantidad <= 0:
            raise DatosInvalidos("Cantidad debe ser positiva")
