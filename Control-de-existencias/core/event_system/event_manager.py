"""
╔════════════════════════════════════════════════════════════════╗
║  ARCHIVO: core/event_system/event_manager.py                  ║
║  FUNCIÓN: Gestor de eventos (Subject en Observer pattern)    ║
╚════════════════════════════════════════════════════════════════╝

PATRÓN: OBSERVER (EventManager = Subject/Publisher)

El EventManager:
  • Mantiene lista de observadores
  • Permite registrar/desregistrar observers
  • Dispara eventos a todos los observadores suscritos
"""

from typing import List, Dict, Set
from core.event_system.event import Event
from core.event_system.observer import Observer


class EventManager:
    """Gestor centralizado de eventos y observadores."""
    
    def __init__(self):
        """Inicializar EventManager."""
        self._observers: Dict[str, Set[Observer]] = {}
    
    def subscribe(self, event_type: str, observer: Observer) -> None:
        """
        Suscribir un observador a un tipo de evento.
        
        Args:
            event_type: Tipo de evento (ej: 'stock_bajo')
            observer: Instancia del observador
        """
        if event_type not in self._observers:
            self._observers[event_type] = set()
        
        self._observers[event_type].add(observer)
        print(f"[EVENT] {observer.__class__.__name__} suscrito a '{event_type}'")
    
    def unsubscribe(self, event_type: str, observer: Observer) -> None:
        """
        Desuscribir un observador de un tipo de evento.
        
        Args:
            event_type: Tipo de evento
            observer: Instancia del observador
        """
        if event_type in self._observers:
            self._observers[event_type].discard(observer)
    
    def emit(self, event: Event) -> None:
        """
        Dispara un evento a todos los observadores suscritos.
        
        Args:
            event: Evento a disparar
        """
        event_type = event.event_type
        
        if event_type not in self._observers:
            return
        
        # Notificar a todos los observadores suscritos
        for observer in self._observers[event_type]:
            try:
                observer.update(event)
            except Exception as e:
                print(f"[ERROR] Observer {observer.__class__.__name__} falló: {e}")
    
    def get_subscribers_count(self, event_type: str) -> int:
        """Obtener cantidad de observadores para un tipo de evento."""
        return len(self._observers.get(event_type, set()))
    
    def __repr__(self):
        summary = ", ".join(
            f"{event_type}({len(observers)})"
            for event_type, observers in self._observers.items()
        )
        return f"EventManager({summary})"


# Instancia global del gestor de eventos
event_manager = EventManager()
