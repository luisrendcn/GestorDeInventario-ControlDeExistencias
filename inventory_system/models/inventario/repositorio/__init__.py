"""
repositorio/__init__.py
=======================
Módulo Repositorio - Gestiona la estructura de datos del inventario.

Responsabilidad:
    - Mantener la colección de productos
    - Proporcionar interfaz de contenedor (__len__, __repr__)
"""

from typing import Dict


class RepositorioMixin:
    """
    Mixin que gestiona la estructura de datos del inventario.
    
    Responsabilidad única:
        Mantener y exponer la colección de productos.
    
    Inicializa:
    - _productos: Dict con los productos en memoria
    - _historial_movimientos: List con el registro de auditoría
    """

    def __init__(self):
        """Inicializa las estructuras de datos del inventario."""
        # Diccionario para acceso O(1) por ID
        self._productos: Dict[str, 'Producto'] = {}
        # Lista para registro de auditoría de movimientos
        self._historial_movimientos: list = []

    def __len__(self) -> int:
        """Retorna el número de productos en el inventario."""
        return len(self._productos)

    def __repr__(self) -> str:
        """Representación en string del inventario."""
        return f"Inventario({len(self._productos)} productos)"


__all__ = ['RepositorioMixin']
