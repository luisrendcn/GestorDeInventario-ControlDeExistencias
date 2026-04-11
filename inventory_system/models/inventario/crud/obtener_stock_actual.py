"""
crud/obtener_stock_actual.py
=============================
Operación: Obtener stock actual de un producto.

Responsabilidad única:
    - Recuperar el stock actual de un producto específico
"""


class ObtenerStockActualMixin:
    """Mixin especializado en consultar stock actual."""

    def obtener_stock_actual(self, producto_id: str) -> int:
        """
        Obtiene el stock actual de un producto.
        
        Args:
            producto_id: ID del producto
            
        Returns:
            Cantidad actual de stock
            
        Raises:
            ValueError: Si el producto no existe
        """
        producto = self.obtener_o_error(producto_id)
        return producto.stock
