"""
producto/propiedades.py
=======================
Responsabilidad única: Definir propiedades derivadas del producto.
"""


class PropiedadesMixin:
    """Mixin especializado en propiedades derivadas."""
    
    @property
    def stock_bajo(self) -> bool:
        """Retorna True si stock está bajo el mínimo."""
        return self.stock <= self.stock_minimo
    
    @property
    def agotado(self) -> bool:
        """Retorna True si stock = 0."""
        return self.stock == 0
    
    @property
    def valor_total(self) -> float:
        """Valor total del producto en stock."""
        return self.precio * self.stock
