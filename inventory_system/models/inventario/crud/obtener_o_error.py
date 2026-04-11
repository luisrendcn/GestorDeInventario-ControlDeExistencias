"""
crud/obtener_o_error.py
=======================
Operación: Obtener un producto por ID (con validación).

Responsabilidad única:
    - Recuperar un producto por su ID
    - Lanzar error si no existe
"""


class ObtenerOErrorMixin:
    """Mixin especializado en obtener productos con validación."""

    def obtener_o_error(self, id: str) -> 'Producto':
        """
        Obtiene un producto por ID o lanza ValueError si no existe.
        
        Esta es la versión "segura" que garantiza obtener un producto válido.
        
        Args:
            id: ID del producto
            
        Returns:
            Producto encontrado
            
        Raises:
            ValueError: Si el producto no existe
        """
        producto = self.obtener(id)
        if producto is None:
            raise ValueError(f"Producto con ID '{id}' no encontrado.")
        return producto
