"""
╔════════════════════════════════════════════════════════════════════════════╗
║              ARCHIVO: core/models/inventario/listar_productos.py           ║
║              RESPONSABILIDAD: Listar todos los productos                  ║
╚════════════════════════════════════════════════════════════════════════════╝

🎯 ÚNICA RESPONSABILIDAD:
   Obtener la lista completa de productos en el inventario.
   
💡 OPERACIÓN:
   • listar_productos: Recuperar todos los productos
"""


class ListarProductosMixin:
    """
    Mixin que agrega operación de listado a Inventario.
    
    RESPONSABILIDAD: 1
    • Obtener la lista de todos los productos
    
    Requiere atributo:
        • self._productos (Dict[str, Producto])
    """
    
    def listar_productos(self) -> list:
        """
        Listar todos los productos del inventario.
        
        Returns:
            Lista de todas las instancias de Producto
        """
        return list(self._productos.values())
