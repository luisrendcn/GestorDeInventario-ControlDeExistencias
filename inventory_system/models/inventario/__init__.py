"""
inventario/
-----------
Módulo de repositorio de inventario organizado por funcionalidad.

Estructura:
    - inventario.py: Clase coordinadora principal
    - crud.py: Operaciones CRUD (agregar, obtener, eliminar)
    - busqueda.py: Búsqueda y listado de productos
    - consultas.py: Consultas y estadísticas
"""

from .inventario import Inventario

__all__ = ['Inventario']
