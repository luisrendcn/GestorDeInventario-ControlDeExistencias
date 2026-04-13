"""
╔════════════════════════════════════════════════════════════════════════════╗
║                  ARCHIVO: core/exceptions/stock_insuficiente.py           ║
║                  RESPONSABILIDAD: Stock insuficiente para operación        ║
╚════════════════════════════════════════════════════════════════════════════╝

🎯 ÚNICA RESPONSABILIDAD:
   Indicar que no hay stock suficiente para satisfacer una operación.
   
💡 CASOS:
   • Realizar salida de stock sin suficiente cantidad
   • Vender más unidades de las disponibles
   • Transferencia de stock sin suficiente inventario
"""

from core.exceptions.inventario_error import InventarioError


class StockInsuficiente(InventarioError):
    """
    No hay stock suficiente para la operación.
    
    RESPONSABILIDAD: 1
    • Indicar que no hay stock para satisfacer la solicitud
    
    Lanzada por:
        • SalidaStrategy.ejecutar()
        • SalidaStrategy.validar()
    """
    pass
