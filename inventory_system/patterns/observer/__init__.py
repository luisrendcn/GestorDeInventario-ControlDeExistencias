"""
observer/
---------
Patrón comportamental: Observer (Observador).

Desacopla el sistema de notificaciones de cambios de stock.

Componentes:
    - ObservadorStock: interfaz abstracta para observadores
    - AlertaConsolaObservador: muestra alertas de stock bajo
    - AlertaStockCriticoObservador: alerta de agotamiento
    - LogObservador: mantiene historial de eventos
    - SujetoStock: publicador que coordina las notificaciones
"""

from .interfaz import ObservadorStock
from .observadores import (
    AlertaConsolaObservador,
    AlertaStockCriticoObservador,
    LogObservador,
)
from .observer import SujetoStock

__all__ = [
    'ObservadorStock',
    'AlertaConsolaObservador',
    'AlertaStockCriticoObservador',
    'LogObservador',
    'SujetoStock',
]
