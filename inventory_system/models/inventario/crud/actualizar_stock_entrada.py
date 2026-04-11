"""
crud/actualizar_stock_entrada.py
==================================
Operación: Registrar entrada de stock.

Responsabilidad única:
    - Incrementar stock de un producto
    - Validar cantidad positiva
    - Registrar movimiento de entrada
"""


class ActualizarStockEntradaMixin:
    """Mixin especializado en registrar entradas de stock."""

    def actualizar_stock_entrada(self, producto_id: str, cantidad: int) -> int:
        """
        Registra una entrada de stock (compra, devolución, reposición, etc).
        
        Valida que:
        - La cantidad sea positiva
        - El producto exista
        
        Args:
            producto_id: ID del producto
            cantidad: Cantidad a agregar (debe ser > 0)
            
        Returns:
            Nuevo stock total después de la entrada
            
        Raises:
            ValueError: Si la cantidad es inválida o producto no existe
        """
        if cantidad <= 0:
            raise ValueError(
                f"Cantidad de entrada debe ser positiva, recibido: {cantidad}"
            )
        
        producto = self.obtener_o_error(producto_id)
        stock_anterior = producto.stock
        producto.agregar_stock(cantidad)
        
        self.registrar_movimiento(producto_id, 'entrada', cantidad)
        
        return producto.stock
