"""
╔════════════════════════════════════════════════════════════════════════════╗
║              ARCHIVO: core/models/inventario/obtener_producto.py           ║
║              RESPONSABILIDAD: Recuperar producto del inventario           ║
╚════════════════════════════════════════════════════════════════════════════╝

🎯 ÚNICA RESPONSABILIDAD:
   Obtener un producto específico del almacén por su ID.
   
💡 OPERACIÓN:
   • obtener_producto: Recuperar producto (READ)
"""

from typing import Optional


class ObtenerProductoMixin:
    """
    Mixin que agrega operación de lectura a Inventario.
    
    RESPONSABILIDAD: 1
    • Recuperar un producto específico por ID
    
    Requiere atributo:
        • self._productos (Dict[str, Producto])
    """
    
    def obtener_producto(self, id: str) -> Optional[object]:
        """
        Obtener producto del inventario por ID.
        
        Args:
            id: Identificador único del producto
            
        Returns:
            Instancia de Producto o None si no existe
        """
        return self._productos.get(id)
