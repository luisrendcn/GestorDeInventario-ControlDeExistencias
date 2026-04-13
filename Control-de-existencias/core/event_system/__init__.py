"""
╔════════════════════════════════════════════════════════════════╗
║  ARCHIVO: core/event_system/__init__.py                       ║
║  FUNCIÓN: Exports del sistema de eventos                     ║
╚════════════════════════════════════════════════════════════════╝
"""

from core.event_system.event import (
    Event,
    StockBajoEvent,
    MovimientoRegistradoEvent,
    ProductoAgotadoEvent,
)

from core.event_system.observer import Observer

from core.event_system.event_manager import EventManager, event_manager

from core.event_system.listeners import (
    AlertasListener,
    AuditoriaListener,
    NotificacionesListener,
)

__all__ = [
    'Event',
    'StockBajoEvent',
    'MovimientoRegistradoEvent',
    'ProductoAgotadoEvent',
    'Observer',
    'EventManager',
    'event_manager',
    'AlertasListener',
    'AuditoriaListener',
    'NotificacionesListener',
]
