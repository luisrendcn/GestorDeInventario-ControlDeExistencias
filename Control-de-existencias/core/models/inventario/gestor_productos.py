"""
╔════════════════════════════════════════════════════════════════════════════╗
║              ARCHIVO: core/models/inventario/gestor_productos.py           ║
║              RESPONSABILIDAD: Orquestar CRUD de productos                 ║
╚════════════════════════════════════════════════════════════════════════════╝

🎯 ÚNICA RESPONSABILIDAD:
   Coordinar los mixins de operaciones CRUD sobre productos.
   
💡 COMPONE:
   • AgregarProductoMixin - Crear producto (CREATE)
   • ObtenerProductoMixin - Leer producto (READ)
   • ListarProductosMixin - Listar productos (READ ALL)
   • EliminarProductoMixin - Borrar producto (DELETE)
   • ExisteProductoMixin - Verificar existencia
"""

from core.models.inventario.agregar_producto import AgregarProductoMixin
from core.models.inventario.obtener_producto import ObtenerProductoMixin
from core.models.inventario.listar_productos import ListarProductosMixin
from core.models.inventario.eliminar_producto import EliminarProductoMixin
from core.models.inventario.existe_producto import ExisteProductoMixin


class GestorProductosMixin(
    AgregarProductoMixin,
    ObtenerProductoMixin,
    ListarProductosMixin,
    EliminarProductoMixin,
    ExisteProductoMixin,
):
    """
    Mixin orquestador de gestión de productos.
    
    RESPONSABILIDAD: 1
    • Combinar mixins de operaciones CRUD
    
    Submixins:
        • AgregarProductoMixin - agregar_producto()
        • ObtenerProductoMixin - obtener_producto()
        • ListarProductosMixin - listar_productos()
        • EliminarProductoMixin - eliminar_producto()
        • ExisteProductoMixin - existe_producto()
    
    Requiere atributo:
        • self._productos (Dict[str, Producto])
    """
    pass
