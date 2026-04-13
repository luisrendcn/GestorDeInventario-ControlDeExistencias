"""
╔════════════════════════════════════════════════════════════════════════════╗
║              ARCHIVO: core/models/producto/reducir_stock.py               ║
║              RESPONSABILIDAD: Operación reducir stock                     ║
╚════════════════════════════════════════════════════════════════════════════╝

🎯 ÚNICA RESPONSABILIDAD:
   Decrementar la cantidad disponible (movimiento de SALIDA).
   
💡 OPERACIÓN:
   • reducir_stock: Disminuir stock en cantidad positiva
"""

from datetime import datetime


class ReducirStockMixin:
    """
    Mixin que agrega operación para disminuir stock.
    
    RESPONSABILIDAD: 1
    • Decrementar stock (operación de SALIDA)
    
    Requiere atributos:
        • self.stock (int)
        • self.updated_at (datetime)
    """
    
    def reducir_stock(self, cantidad: int):
        """
        Decrementar stock (SALIDA).
        
        Args:
            cantidad: Cantidad a restar (debe ser positiva)
        """
        self.stock -= cantidad
        self.updated_at = datetime.now()
