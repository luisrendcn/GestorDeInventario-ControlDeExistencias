"""
╔════════════════════════════════════════════════════════════════════════════╗
║              ARCHIVO: core/models/producto/agotado.py                     ║
║              RESPONSABILIDAD: Propiedad de stock agotado                  ║
╚════════════════════════════════════════════════════════════════════════════╝

🎯 ÚNICA RESPONSABILIDAD:
   Calcular si el stock está completamente agotado.
   
💡 LÓGICA:
   • agotado = stock == 0
"""


class AgotadoMixin:
    """
    Mixin que agrega propiedad agotado a Producto.
    
    RESPONSABILIDAD: 1
    • Determinar si el stock está agotado
    
    Requiere atributo:
        • self.stock (int)
    """
    
    @property
    def agotado(self) -> bool:
        """
        ¿Stock es completamente cero?
        
        Returns:
            True si stock == 0, False si hay cantidad
        """
        return self.stock == 0
