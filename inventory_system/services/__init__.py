"""
services/
---------
Módulo de servicios de negocio para la gestión de inventario.

Contiene:
    - inventario_service.py: Lógica de gestión de inventario
    - transaccion_service.py: Lógica de transacciones
    - import_service.py: Importación de productos desde Excel
"""

from .inventario_service import InventarioService
from .transaccion_service import TransaccionService
from .import_service import ImportadorExcel, ImportResult

__all__ = [
    'InventarioService',
    'TransaccionService',
    'ImportadorExcel',
    'ImportResult',
]
