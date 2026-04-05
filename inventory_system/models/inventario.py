"""
models/inventario.py
--------------------
Clase de dominio que representa el inventario completo.
Actúa como repositorio en memoria de todos los productos.

Aplica:
- Alta cohesión: gestiona únicamente la colección de productos
- Bajo acoplamiento: no conoce la lógica de negocio
"""

from typing import Dict, List, Optional
from .producto import Producto


class Inventario:
    """
    Repositorio en memoria de productos.
    Gestiona el almacenamiento, búsqueda y eliminación de productos.
    """

    def __init__(self):
        # Usamos un dict para acceso O(1) por ID
        self._productos: Dict[str, Producto] = {}

    # --- CRUD básico ---

    def agregar(self, producto: Producto) -> None:
        """Agrega un nuevo producto. Lanza error si el ID ya existe."""
        if producto.id in self._productos:
            raise ValueError(f"Ya existe un producto con ID '{producto.id}'.")
        self._productos[producto.id] = producto

    def obtener(self, id: str) -> Optional[Producto]:
        """Retorna el producto por ID, o None si no existe."""
        return self._productos.get(id)

    def obtener_o_error(self, id: str) -> Producto:
        """Retorna el producto por ID. Lanza ValueError si no existe."""
        producto = self.obtener(id)
        if producto is None:
            raise ValueError(f"Producto con ID '{id}' no encontrado.")
        return producto

    def eliminar(self, id: str) -> Producto:
        """Elimina y retorna el producto. Lanza error si no existe."""
        if id not in self._productos:
            raise ValueError(f"Producto con ID '{id}' no encontrado.")
        return self._productos.pop(id)

    def listar_todos(self) -> List[Producto]:
        """Retorna lista de todos los productos."""
        return list(self._productos.values())

    def buscar_por_nombre(self, nombre: str) -> List[Producto]:
        """Búsqueda parcial por nombre (case-insensitive)."""
        termino = nombre.lower()
        return [p for p in self._productos.values() if termino in p.nombre.lower()]

    def productos_con_stock_bajo(self) -> List[Producto]:
        """Retorna productos cuyo stock está por debajo del mínimo."""
        return [p for p in self._productos.values() if p.stock_bajo]

    def existe(self, id: str) -> bool:
        """Comprueba si existe un producto con ese ID."""
        return id in self._productos

    def total_productos(self) -> int:
        """Número total de productos en el inventario."""
        return len(self._productos)

    def valor_total_inventario(self) -> float:
        """Calcula el valor total del inventario (precio × stock)."""
        return sum(p.precio * p.stock for p in self._productos.values())

    def __len__(self) -> int:
        return len(self._productos)

    def __repr__(self) -> str:
        return f"Inventario({len(self._productos)} productos)"
