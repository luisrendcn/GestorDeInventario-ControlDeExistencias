"""
producto/stock.py
=================
Responsabilidad única: Operaciones de modificación de stock.
"""


class StockMixin:
    """Mixin especializado en operaciones de stock."""
    
    def agregar_stock(self, cantidad: int) -> None:
        """Incrementar stock (entrada)."""
        if cantidad <= 0:
            raise ValueError("Cantidad debe ser positiva")
        self.stock += cantidad
    
    def reducir_stock(self, cantidad: int) -> None:
        """Reducir stock (salida)."""
        if cantidad <= 0:
            raise ValueError("Cantidad debe ser positiva")
        if cantidad > self.stock:
            raise ValueError(f"Stock insuficiente. Disponible: {self.stock}, solicitado: {cantidad}")
        self.stock -= cantidad
    
    def ajustar_stock(self, nuevo_stock: int) -> None:
        """Ajustar stock a un valor específico (auditoría)."""
        if nuevo_stock < 0:
            raise ValueError("Stock no puede ser negativo")
        self.stock = nuevo_stock
