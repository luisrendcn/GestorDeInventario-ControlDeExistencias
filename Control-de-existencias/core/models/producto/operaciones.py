"""
╔════════════════════════════════════════════════════════════════════════════╗
║              ARCHIVO: core/models/producto/operaciones.py                 ║
║              RESPONSABILIDAD: Orquestar operaciones de stock              ║
╚════════════════════════════════════════════════════════════════════════════╝

🎯 ÚNICA RESPONSABILIDAD:
   Combinar los mixins de operaciones de mutación de stock.
   
💡 COMPONE:
   • AgregarStockMixin - Incrementar stock (ENTRADA)
   • ReducirStockMixin - Decrementar stock (SALIDA)
   • EstablecerStockMixin - Asignar stock exacto (AJUSTE)
"""

from core.models.producto.agregar_stock import AgregarStockMixin
from core.models.producto.reducir_stock import ReducirStockMixin
from core.models.producto.establecer_stock import EstablecerStockMixin


class OperacionesMixin(AgregarStockMixin, ReducirStockMixin, EstablecerStockMixin):
    """
    Mixin orquestador de operaciones de stock.
    
    RESPONSABILIDAD: 1
    • Combinar mixins de mutación de stock
    
    Submixins:
        • AgregarStockMixin - agregar_stock()
        • ReducirStockMixin - reducir_stock()
        • EstablecerStockMixin - establecer_stock()
    
    Requiere atributos:
        • self.stock (int)
        • self.updated_at (datetime)
    """
    pass
