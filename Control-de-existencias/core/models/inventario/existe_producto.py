"""
╔════════════════════════════════════════════════════════════════════════════╗
║              ARCHIVO: core/models/inventario/existe_producto.py            ║
║              RESPONSABILIDAD: Verificar existencia de producto            ║
╚════════════════════════════════════════════════════════════════════════════╝

🎯 ÚNICA RESPONSABILIDAD:
   Comprobar si un producto existe en el almacén.
   
💡 OPERACIÓN:
   • existe_producto: Verificar presencia de producto
"""


class ExisteProductoMixin:
    """
    Mixin que agrega operación de verificación a Inventario.
    
    RESPONSABILIDAD: 1
    • Verificar si un producto existe en el almacén
    
    Requiere atributo:
        • self._productos (Dict[str, Producto])
    """
    
    def existe_producto(self, id: str) -> bool:
        """
        Verificar si un producto existe en el inventario.
        
        Args:
            id: Identificador único del producto
            
        Returns:
            True si existe, False si no existe
        """
        return id in self._productos

