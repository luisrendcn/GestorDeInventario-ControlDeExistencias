"""
╔════════════════════════════════════════════════════════════════════════════╗
║              ARCHIVO: core/models/producto/establecer_stock.py            ║
║              RESPONSABILIDAD: Operación establecer stock                  ║
╚════════════════════════════════════════════════════════════════════════════╝

🎯 ÚNICA RESPONSABILIDAD:
   Asignar un valor exacto de stock (movimiento de AJUSTE).
   
💡 OPERACIÓN:
   • establecer_stock: Fijar stock a cantidad específica
"""

from datetime import datetime


class EstablecerStockMixin:
    """
    Mixin que agrega operación para establecer stock exacto.
    
    RESPONSABILIDAD: 1
    • Asignar stock exacto (operación de AJUSTE)
    
    Requiere atributos:
        • self.stock (int)
        • self.updated_at (datetime)
    """
    
    def establecer_stock(self, nuevo_stock: int):
        """
        Establecer stock a un valor exacto (AJUSTE).
        
        Args:
            nuevo_stock: Cantidad exacta a asignar
        """
        self.stock = nuevo_stock
        self.updated_at = datetime.now()
