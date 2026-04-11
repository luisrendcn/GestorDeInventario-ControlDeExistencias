"""
inventario/inventario.py
========================
Orquestador de Inventario - Solo coordina los mixins.

Responsabilidad única:
    - Orquestar la composición de funcionalidades
    - Proporcionar interfaz unificada

Hereda de:
    - RepositorioMixin: Gestión de estructura de datos (_productos, _historial_movimientos)
    - HistorialMixin: Auditoría de movimientos (registrar, obtener, limpiar)
    - CRUDMixin: Operaciones CRUD
    - BúsquedaMixin: Búsqueda y listado
    - ConsultasMixin: Consultas y análisis

Cada responsabilidad está en su propio mixin, en su propio archivo.
"""

from .repositorio import RepositorioMixin
from .historial import HistorialMixin
from .crud import CRUDMixin
from .busqueda import BúsquedaMixin
from .consultas import ConsultasMixin


class Inventario(
    RepositorioMixin,
    HistorialMixin,
    CRUDMixin,
    BúsquedaMixin,
    ConsultasMixin,
):
    """
    Inventario de productos con control de existencias.
    
    Responsabilidad única:
        Orquestar la composición de funcionalidades especializadas.
    
    Funcionalidades (heredadas):
        - Repositorio: Estructura de datos, __len__, __repr__
        - Historial: Auditoría de movimientos
        - CRUD: Operaciones básicas
        - Búsqueda: Búsqueda y listado
        - Consultas: Análisis y reportes
    
    Uso:
        inv = Inventario()
        inv.agregar(producto)           # CRUD
        inv.listar_todos()              # Búsqueda
        inv.obtener_reporte_stock()     # Consultas
        inv.obtener_historial()         # Historial
    """
    pass
