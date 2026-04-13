"""
╔════════════════════════════════════════════════════════════════════════════╗
║              ARCHIVO: core/models/producto/valor_total.py                 ║
║              RESPONSABILIDAD: Propiedad de valor total                    ║
╚════════════════════════════════════════════════════════════════════════════╝

🎯 ÚNICA RESPONSABILIDAD:
   Calcular el valor económico total del producto en stock.
   
💡 LÓGICA:
   • valor_total = precio * stock (cálculo de inventario)
"""


class ValorTotalMixin:
    """
    Mixin que agrega propiedad valor_total a Producto.
    
    RESPONSABILIDAD: 1
    • Calcular el valor económico del stock actual
    
    Requiere atributos:
        • self.precio (float)
        • self.stock (int)
    """
    
    @property
    def valor_total(self) -> float:
        """
        Valor económico total del producto en stock.
        
        Returns:
            float: precio * stock (valor de inventario)
        """
        return self.precio * self.stock
