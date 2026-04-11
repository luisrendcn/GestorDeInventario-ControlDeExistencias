"""
inventario/crud.py
==================
Mixin que maneja operaciones CRUD básicas del inventario y control de existencias.

Responsabilidad:
    - Operaciones de creación, lectura, actualización, eliminación
    - Registro de entradas y salidas de stock
    - Validación de stock no-negativo
    - Persistencia de cambios
"""

from typing import Optional
from datetime import datetime


class CRUDMixin:
    """
    Mixin para operaciones CRUD en el inventario.
    Incluye control de existencias (entrada/salida de stock).
    """

    def agregar(self, producto: 'Producto') -> None:
        """
        Agrega un nuevo producto. Lanza error si el ID ya existe.
        
        Args:
            producto: Producto a agregar
            
        Raises:
            ValueError: Si el producto con ese ID ya existe
        """
        if producto.id in self._productos:
            raise ValueError(f"Ya existe un producto con ID '{producto.id}'.")
        self._productos[producto.id] = producto
        self.registrar_movimiento(producto.id, 'inicial', producto.stock)

    def obtener(self, id: str) -> Optional['Producto']:
        """
        Retorna el producto por ID, o None si no existe.
        
        Args:
            id: ID del producto
            
        Returns:
            Producto si existe, None en caso contrario
        """
        return self._productos.get(id)

    def obtener_o_error(self, id: str) -> 'Producto':
        """
        Retorna el producto por ID. Lanza ValueError si no existe.
        
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

    def eliminar(self, id: str) -> 'Producto':
        """
        Elimina y retorna el producto. Lanza error si no existe.
        
        Args:
            id: ID del producto a eliminar
            
        Returns:
            Producto eliminado
            
        Raises:
            ValueError: Si el producto no existe
        """
        if id not in self._productos:
            raise ValueError(f"Producto con ID '{id}' no encontrado.")
        producto = self._productos.pop(id)
        self.registrar_movimiento(id, 'eliminacion', producto.stock)
        return producto

    def actualizar_stock_entrada(self, producto_id: str, cantidad: int) -> int:
        """
        Registra una entrada de stock (compra, devolución, etc).
        
        Args:
            producto_id: ID del producto
            cantidad: Cantidad a agregar (debe ser positiva)
            
        Returns:
            Nuevo stock total
            
        Raises:
            ValueError: Si la cantidad es inválida o el producto no existe
        """
        if cantidad <= 0:
            raise ValueError(f"Cantidad de entrada debe ser positiva, recibido: {cantidad}")
        
        producto = self.obtener_o_error(producto_id)
        stock_anterior = producto.stock
        producto.agregar_stock(cantidad)
        
        self.registrar_movimiento(producto_id, 'entrada', cantidad)
        
        return producto.stock

    def actualizar_stock_salida(self, producto_id: str, cantidad: int) -> int:
        """
        Registra una salida de stock (venta, ajuste negativo, etc).
        
        Valida que:
        - La cantidad sea positiva
        - El producto exista
        - No resulte en stock negativo
        
        Args:
            producto_id: ID del producto
            cantidad: Cantidad a restar (debe ser positiva)
            
        Returns:
            Nuevo stock total
            
        Raises:
            ValueError: Si la cantidad es inválida, el producto no existe o insuficiente stock
        """
        if cantidad <= 0:
            raise ValueError(f"Cantidad de salida debe ser positiva, recibido: {cantidad}")
        
        producto = self.obtener_o_error(producto_id)
        
        if producto.stock < cantidad:
            raise ValueError(
                f"Stock insuficiente para '{producto.nombre}' (ID: {producto_id}). "
                f"Stock disponible: {producto.stock}, solicitado: {cantidad}"
            )
        
        stock_anterior = producto.stock
        producto.reducir_stock(cantidad)
        
        self.registrar_movimiento(producto_id, 'salida', cantidad)
        
        return producto.stock

    def obtener_stock_actual(self, producto_id: str) -> int:
        """
        Obtiene el stock actual de un producto.
        
        Args:
            producto_id: ID del producto
            
        Returns:
            Stock actual
            
        Raises:
            ValueError: Si el producto no existe
        """
        producto = self.obtener_o_error(producto_id)
        return producto.stock

    def validar_stock_no_negativo(self, producto_id: str) -> bool:
        """
        Valida que el stock de un producto no sea negativo.
        
        Args:
            producto_id: ID del producto
            
        Returns:
            True si el stock es válido (>= 0)
            
        Raises:
            ValueError: Si el producto no existe
        """
        producto = self.obtener_o_error(producto_id)
        if producto.stock < 0:
            raise ValueError(
                f"INCONSISTENCIA: Stock negativo detectado en '{producto.nombre}' "
                f"(ID: {producto_id}). Stock: {producto.stock}"
            )
        return True
