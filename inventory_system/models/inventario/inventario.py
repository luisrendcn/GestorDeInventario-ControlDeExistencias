"""
inventario/inventario.py
========================
Repositorio de inventario organizado con mixins.

Responsabilidad:
    - Coordinar la colección de productos
    - Delegar operaciones a mixins especializados

Aplica:
    - Alta cohesión: gestiona únicamente la colección de productos
    - Bajo acoplamiento: no conoce la lógica de negocio
    - Separación de responsabilidades con mixins
"""

from typing import Dict
from .crud import CRUDMixin
from .busqueda import BúsquedaMixin
from .consultas import ConsultasMixin


class Inventario(CRUDMixin, BúsquedaMixin, ConsultasMixin):
    """
    Repositorio en memoria de productos.
    
    Hereda funcionalidad de:
    - CRUDMixin: agregar, obtener, obtener_o_error, eliminar
    - BúsquedaMixin: listar_todos, buscar_por_nombre
    - ConsultasMixin: existe, total_productos, valor_total_inventario, productos_con_stock_bajo
    """

    def __init__(self):
        # Usamos un dict para acceso O(1) por ID
        self._productos: Dict[str, Producto] = {}

    def __len__(self) -> int:
        return len(self._productos)

    def __repr__(self) -> str:
        return f"Inventario({len(self._productos)} productos)"
