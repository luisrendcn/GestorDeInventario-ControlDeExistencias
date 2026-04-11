"""
crud/agregar.py
===============
Operación: Agregar un nuevo producto al inventario.

Responsabilidad única:
    - Crear un nuevo registro de producto
    - Validar que no exista duplicado
    - Registrar movimiento inicial
"""


class AgregarMixin:
    """Mixin especializado en agregar productos al inventario."""

    def agregar(self, producto: 'Producto') -> None:
        """
        Agrega un nuevo producto al inventario.
        
        Lanza error si ya existe un producto con el mismo ID.
        Registra automáticamente el movimiento inicial de stock.
        
        Args:
            producto: Producto a agregar al inventario
            
        Raises:
            ValueError: Si ya existe producto con ese ID
        """
        if producto.id in self._productos:
            raise ValueError(f"Ya existe un producto con ID '{producto.id}'.")
        
        self._productos[producto.id] = producto
        self.registrar_movimiento(producto.id, 'inicial', producto.stock)
