"""
╔════════════════════════════════════════════════════════════════════════════╗
║              ARCHIVO: core/models/inventario/agregar_producto.py           ║
║              RESPONSABILIDAD: Agregar producto al inventario              ║
╚════════════════════════════════════════════════════════════════════════════╝

🎯 ÚNICA RESPONSABILIDAD:
   Registrar un nuevo producto en el almacén de inventario.
   
💡 OPERACIÓN:
   • agregar_producto: Almacenar producto (CREATE)
"""


class AgregarProductoMixin:
    """
    Mixin que agrega operación de crear producto a Inventario.
    
    RESPONSABILIDAD: 1
    • Registrar un nuevo producto en el almacén
    
    Requiere atributo:
        • self._productos (Dict[str, Producto])
    """
    
    def agregar_producto(self, producto):
        """
        Agregar producto al inventario.
        
        Args:
            producto: Instancia de Producto a registrar
        """
        self._productos[producto.id] = producto
