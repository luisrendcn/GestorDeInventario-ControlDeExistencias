"""Clase Inventario con gestión de productos y historial separadas."""

from typing import Dict

from core.models.inventario.gestor_productos import GestorProductosMixin
from core.models.inventario.gestor_historial import GestorHistorialMixin


class Inventario(GestorProductosMixin, GestorHistorialMixin):
    """
    Orquestador de inventario.
    
    Coordina operaciones de stock y auditoría organizadas en mixins.
    
    RESPONSABILIDADES (composición de 2 mixins principales):
      1️⃣  GestorProductosMixin - CRUD de productos
            - AgregarProductoMixin
            - ObtenerProductoMixin
            - ListarProductosMixin
            - EliminarProductoMixin
            - ExisteProductoMixin
      
      2️⃣  GestorHistorialMixin - Auditoría de movimientos
            - RegistrarMovimientoMixin
            - ObtenerHistorialMixin
    
    ALMACENAMIENTO:
      • _productos: Diccionario de productos (id → Producto)
      • _historial: Lista de movimientos realizados
    """
    
    def __init__(self):
        self._productos: Dict[str, object] = {}
        self._historial: list = []
    
    def __len__(self) -> int:
        """Cantidad de productos en el inventario."""
        return len(self._productos)
    
    def __repr__(self) -> str:
        return f"Inventario({len(self)} productos)"
