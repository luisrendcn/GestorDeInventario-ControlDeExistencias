"""
crud/actualizar_stock_salida.py
================================
Operación: Registrar salida de stock.

Responsabilidad única:
    - Decrementar stock de un producto
    - Validar cantidad positiva y stock suficiente
    - Registrar movimiento de salida
"""


class ActualizarStockSalidaMixin:
    """Mixin especializado en registrar salidas de stock."""

    def actualizar_stock_salida(self, producto_id: str, cantidad: int) -> int:
        """
        Registra una salida de stock (venta, daño, ajuste negativo, etc).
        
        Valida que:
        - La cantidad sea positiva
        - El producto exista
        - Haya stock suficiente (no permite negativos)
        
        Args:
            producto_id: ID del producto
            cantidad: Cantidad a restar (debe ser > 0)
            
        Returns:
            Nuevo stock total después de la salida
            
        Raises:
            ValueError: Si hay inconsistencias o stock insuficiente
        """
        if cantidad <= 0:
            raise ValueError(
                f"Cantidad de salida debe ser positiva, recibido: {cantidad}"
            )
        
        producto = self.obtener_o_error(producto_id)
        
        if producto.stock < cantidad:
            raise ValueError(
                f"Stock insuficiente para '{producto.nombre}' (ID: {producto_id}). "
                f"Stock disponible: {producto.stock}, solicitado: {cantidad}"
            )
        
        stock_anterior = producto.stock
        producto.reducir_stock(cantidad)
        
        self.registrar_movimiento(producto_id, 'salida', cantidad)
        
        return producto.stock
