"""
╔════════════════════════════════════════════════════════════════════════════╗
║                  ARCHIVO: core/exceptions/producto_no_encontrado.py       ║
║                  RESPONSABILIDAD: Producto no existe                       ║
╚════════════════════════════════════════════════════════════════════════════╝

🎯 ÚNICA RESPONSABILIDAD:
   Indicar que el producto especificado no existe en el inventario.
   
💡 CASOS:
   • Buscar producto que no existe
   • Actualizar producto no existente
   • Eliminar producto no existente
"""

from core.exceptions.inventario_error import InventarioError


class ProductoNoEncontrado(InventarioError):
    """
    El producto no existe en el inventario.
    
    RESPONSABILIDAD: 1
    • Indicar que el producto especificado no existe
    
    Lanzada por:
        • CrearProductoService.crear()
        • ObtenerProductoService.obtener()
        • ActualizarProductoService.actualizar()
        • EliminarProductoService.eliminar()
    """
    pass
