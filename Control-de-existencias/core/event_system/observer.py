"""
╔════════════════════════════════════════════════════════════════╗
║  ARCHIVO: core/event_system/observer.py                       ║
║  FUNCIÓN: Interface Observer (abstracta)                      ║
╚════════════════════════════════════════════════════════════════╝

PATRÓN: OBSERVER (Define contrato para Observers)
"""

from abc import ABC, abstractmethod
from core.event_system.event import Event


class Observer(ABC):
    """Interface para Observer pattern."""
    
    @abstractmethod
    def update(self, event: Event) -> None:
        """
        Método llamado cuando ocurre un evento.
        
        Args:
            event: El evento que ocurrió
        """
        pass
