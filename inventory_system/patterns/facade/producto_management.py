"""
facade/producto_management.py
=============================
Mixin: Gestión de productos.

Responsabilidad:
    - Crear productos usando Factory
    - Editar, eliminar, obtener productos
    - Listar y buscar productos
    - Identificar productos con stock bajo
"""

from typing import Dict, Any, List, Optional
from models import Producto
from patterns.factory import FactoryManager


class ProductoManagementMixin:
    """Mixin para operaciones de gestión de productos."""

    def crear_producto(self, tipo: str, datos: Dict[str, Any]) -> Producto:
        """
        Crea un producto usando el Factory Method y lo agrega al inventario.
        """
        producto = FactoryManager.crear_producto(tipo, datos)
        self._inventario_service.agregar_producto(producto)
        return producto

    def editar_producto(self, id: str, nuevos_datos: Dict[str, Any]) -> Producto:
        """Actualiza los campos editables de un producto existente."""
        return self._inventario_service.editar_producto(id, nuevos_datos)

    def eliminar_producto(self, id: str) -> Producto:
        """Elimina un producto del inventario."""
        return self._inventario_service.eliminar_producto(id)

    def obtener_producto(self, id: str) -> Optional[Producto]:
        """Retorna un producto por su ID."""
        return self._inventario.obtener(id)

    def listar_productos(self) -> List[Producto]:
        """Lista todos los productos del inventario."""
        return self._inventario.listar_todos()

    def buscar_productos(self, nombre: str) -> List[Producto]:
        """Búsqueda por nombre parcial."""
        return self._inventario.buscar_por_nombre(nombre)

    def productos_stock_bajo(self) -> List[Producto]:
        """Retorna productos con stock por debajo del mínimo."""
        return self._inventario.productos_con_stock_bajo()
