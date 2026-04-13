"""
╔════════════════════════════════════════════════════════════════╗
║  ARCHIVO: core/event_system/event.py                          ║
║  FUNCIÓN: Clases de eventos para patrón Observer              ║
╚════════════════════════════════════════════════════════════════╝

PATRÓN: OBSERVER (Define notificaciones de eventos)
"""

from typing import Dict, Any
from datetime import datetime


class Event:
    """Clase base para todos los eventos."""
    
    def __init__(self, event_type: str, data: Dict[str, Any] = None):
        """
        Crear un evento.
        
        Args:
            event_type: Tipo de evento (ej: 'stock_bajo', 'movimiento_registrado')
            data: Datos asociados al evento
        """
        self.event_type = event_type
        self.data = data or {}
        self.timestamp = datetime.now().isoformat()
    
    def __repr__(self):
        return f"Event('{self.event_type}', timestamp='{self.timestamp}')"


class StockBajoEvent(Event):
    """Evento cuando el stock cae por debajo del mínimo."""
    
    def __init__(self, producto_id: str, nombre: str, stock: int, stock_minimo: int):
        """Crear evento de stock bajo."""
        super().__init__(
            event_type='stock_bajo',
            data={
                'producto_id': producto_id,
                'nombre': nombre,
                'stock': stock,
                'stock_minimo': stock_minimo,
            }
        )


class MovimientoRegistradoEvent(Event):
    """Evento cuando se registra un movimiento de stock."""
    
    def __init__(self, producto_id: str, tipo: str, cantidad: int, 
                 stock_anterior: int, stock_nuevo: int):
        """Crear evento de movimiento registrado."""
        super().__init__(
            event_type='movimiento_registrado',
            data={
                'producto_id': producto_id,
                'tipo': tipo,
                'cantidad': cantidad,
                'stock_anterior': stock_anterior,
                'stock_nuevo': stock_nuevo,
            }
        )


class ProductoAgotadoEvent(Event):
    """Evento cuando un producto se agota completamente."""
    
    def __init__(self, producto_id: str, nombre: str):
        """Crear evento de producto agotado."""
        super().__init__(
            event_type='producto_agotado',
            data={
                'producto_id': producto_id,
                'nombre': nombre,
            }
        )
