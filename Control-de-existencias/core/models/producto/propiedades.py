"""
╔════════════════════════════════════════════════════════════════════════════╗
║              ARCHIVO: core/models/producto/propiedades.py                 ║
║              RESPONSABILIDAD: Orquestar propiedades derivadas             ║
╚════════════════════════════════════════════════════════════════════════════╝

🎯 ÚNICA RESPONSABILIDAD:
   Combinar los mixins de propiedades computadas.
   
💡 COMPONE:
   • StockBajoMixin - Indicador de stock bajo
   • AgotadoMixin - Indicador de stock agotado
   • ValorTotalMixin - Cálculo de valor económico
"""

from core.models.producto.stock_bajo import StockBajoMixin
from core.models.producto.agotado import AgotadoMixin
from core.models.producto.valor_total import ValorTotalMixin


class PropiedadesMixin(StockBajoMixin, AgotadoMixin, ValorTotalMixin):
    """
    Mixin orquestador de propiedades derivadas.
    
    RESPONSABILIDAD: 1
    • Combinar mixins de propiedades computadas
    
    Submixins:
        • StockBajoMixin - stock_bajo property
        • AgotadoMixin - agotado property
        • ValorTotalMixin - valor_total property
    
    Requiere atributos:
        • self.stock (int)
        • self.stock_minimo (int)
        • self.precio (float)
    """
    pass

