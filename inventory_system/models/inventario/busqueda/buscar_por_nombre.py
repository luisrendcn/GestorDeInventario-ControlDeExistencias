"""
busqueda/buscar_por_nombre.py
=============================
Operación: Búsqueda parcial de productos por nombre.

Responsabilidad única:
    - Realizar búsquedas case-insensitive por nombre de producto
"""

from typing import List


class BuscarPorNombreMixin:
    """Mixin especializado en búsqueda por nombre."""

    def buscar_por_nombre(self, nombre: str) -> List['Producto']:
        """
        Búsqueda parcial por nombre (case-insensitive).
        
        Busca productos cuyo nombre contenga el término especificado,
        sin importar mayúsculas/minúsculas.
        
        Args:
            nombre: Término de búsqueda
            
        Returns:
            Lista de productos que coinciden con el término
        """
        termino = nombre.lower()
        return [
            p for p in self._productos.values() 
            if termino in p.nombre.lower()
        ]
