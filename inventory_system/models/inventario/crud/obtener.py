"""
crud/obtener.py
===============
Operación: Obtener un producto por ID (sin excepciones).

Responsabilidad única:
    - Recuperar un producto por su ID
    - Retornar None si no existe (no lanza errores)
"""

from typing import Optional


class ObtenerMixin:
    """Mixin especializado en obtener productos de forma segura."""

    def obtener(self, id: str) -> Optional['Producto']:
        """
        Obtiene un producto por ID sin lanzar excepciones.
        
        Args:
            id: ID del producto a recuperar
            
        Returns:
            Producto si existe, None en caso contrario
        """
        return self._productos.get(id)
