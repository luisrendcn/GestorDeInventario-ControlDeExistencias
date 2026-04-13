"""
╔════════════════════════════════════════════════════════════════════════════╗
║              ARCHIVO: core/models/producto/agregar_stock.py               ║
║              RESPONSABILIDAD: Operación agregar stock                     ║
╚════════════════════════════════════════════════════════════════════════════╝

🎯 ÚNICA RESPONSABILIDAD:
   Incrementar la cantidad disponible (movimiento de ENTRADA).
   
💡 OPERACIÓN:
   • agregar_stock: Aumentar stock en cantidad positiva
"""

from datetime import datetime


class AgregarStockMixin:
    """
    Mixin que agrega operación para aumentar stock.
    
    RESPONSABILIDAD: 1
    • Incrementar stock (operación de ENTRADA)
    
    Requiere atributos:
        • self.stock (int)
        • self.updated_at (datetime)
    """
    
    def agregar_stock(self, cantidad: int):
        """
        Incrementar stock (ENTRADA).
        
        Args:
            cantidad: Cantidad a agregar (debe ser positiva)
        """
        self.stock += cantidad
        self.updated_at = datetime.now()
