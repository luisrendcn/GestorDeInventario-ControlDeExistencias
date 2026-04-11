"""
crud/validar_stock_no_negativo.py
==================================
Operación: Validar integridad de stock.

Responsabilidad única:
    - Verificar que el stock sea no-negativo
    - Detectar inconsistencias en la BD
"""


class ValidarStockNoNegativoMixin:
    """Mixin especializado en validación de integridad de stock."""

    def validar_stock_no_negativo(self, producto_id: str) -> bool:
        """
        Valida que el stock de un producto sea no-negativo (>= 0).
        
        Detecta inconsistencias que podrían indicar errores en la lógica
        de actualización de stock.
        
        Args:
            producto_id: ID del producto a validar
            
        Returns:
            True si el stock es válido (>= 0)
            
        Raises:
            ValueError: Si el producto no existe o stock < 0
        """
        producto = self.obtener_o_error(producto_id)
        
        if producto.stock < 0:
            raise ValueError(
                f"⚠️ INCONSISTENCIA: Stock negativo detectado en "
                f"'{producto.nombre}' (ID: {producto_id}). "
                f"Stock actual: {producto.stock}\n"
                f"Esto indica un error en la lógica de actualización."
            )
        
        return True
