"""
╔════════════════════════════════════════════════════════════════════════════╗
║              ARCHIVO: core/models/inventario/eliminar_producto.py          ║
║              RESPONSABILIDAD: Eliminar producto del inventario            ║
╚════════════════════════════════════════════════════════════════════════════╝

🎯 ÚNICA RESPONSABILIDAD:
   Remover un producto del almacén de inventario.
   
💡 OPERACIÓN:
   • eliminar_producto: Borrar producto (DELETE)
"""


class EliminarProductoMixin:
    """
    Mixin que agrega operación de eliminar a Inventario.
    
    RESPONSABILIDAD: 1
    • Remover un producto del almacén
    
    Requiere atributo:
        • self._productos (Dict[str, Producto])
    """
    
    def eliminar_producto(self, id: str) -> bool:
        """
        Eliminar producto del inventario.
        
        Args:
            id: Identificador único del producto
            
        Returns:
            True si fue eliminado, False si no existía
        """
        if id in self._productos:
            del self._productos[id]
            return True
        return False
