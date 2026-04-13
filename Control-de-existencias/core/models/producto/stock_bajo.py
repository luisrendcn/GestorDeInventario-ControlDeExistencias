"""
╔════════════════════════════════════════════════════════════════════════════╗
║              ARCHIVO: core/models/producto/stock_bajo.py                  ║
║              RESPONSABILIDAD: Propiedad de stock bajo                     ║
╚════════════════════════════════════════════════════════════════════════════╝

🎯 ÚNICA RESPONSABILIDAD:
   Calcular si el stock está por debajo del mínimo recomendado.
   
💡 LÓGICA:
   • stock_bajo = 0 < stock <= stock_minimo
"""


class StockBajoMixin:
    """
    Mixin que agrega propiedad stock_bajo a Producto.
    
    RESPONSABILIDAD: 1
    • Determinar si el stock está bajo (alerta)
    
    Requiere atributos:
        • self.stock (int)
        • self.stock_minimo (int)
    """
    
    @property
    def stock_bajo(self) -> bool:
        """
        ¿Stock está por debajo del mínimo recomendado?
        
        Returns:
            True si 0 < stock <= stock_minimo, False en caso contrario
        """
        return self.stock <= self.stock_minimo and self.stock > 0
