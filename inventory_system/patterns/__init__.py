"""
patterns/
---------
Módulo de patrones de diseño implementados en el sistema.

Contains:
    - Factory: patrón de creación para productos (4 módulos)
    - Observer: patrón de comportamiento para notificaciones (4 módulos)
    - Facade: patrón estructural para acceso unificado (4 módulos)
"""

from .facade import SistemaInventarioFacade
from .factory import FactoryManager
from .observer import (
    SujetoStock,
    AlertaConsolaObservador,
    AlertaStockCriticoObservador,
    LogObservador,
)

__all__ = [
    'SistemaInventarioFacade',
    'FactoryManager',
    'SujetoStock',
    'AlertaConsolaObservador',
    'AlertaStockCriticoObservador',
    'LogObservador',
]
