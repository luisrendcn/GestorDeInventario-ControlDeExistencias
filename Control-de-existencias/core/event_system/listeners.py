"""
╔════════════════════════════════════════════════════════════════╗
║  ARCHIVO: core/event_system/listeners.py                      ║
║  FUNCIÓN: Implementaciones concretas de Observer              ║
╚════════════════════════════════════════════════════════════════╝

PATRÓN: OBSERVER (Listeners/Observers concretos)

Diferentes formas de reaccionar a eventos del inventario:
  • AlertasListener - Genera alertas
  • AuditoriaListener - Registra eventos en auditoría
  • NotificacionesListener - Envía notificaciones
"""

from core.event_system.observer import Observer
from core.event_system.event import Event, StockBajoEvent, ProductoAgotadoEvent


class AlertasListener(Observer):
    """Observer que genera alertas cuando ocurren eventos críticos."""
    
    def update(self, event: Event) -> None:
        """Procesar evento y generar alertas si corresponde."""
        if isinstance(event, StockBajoEvent):
            self._alerta_stock_bajo(event)
        elif isinstance(event, ProductoAgotadoEvent):
            self._alerta_producto_agotado(event)
    
    def _alerta_stock_bajo(self, event: StockBajoEvent) -> None:
        """Generar alerta de stock bajo."""
        data = event.data
        print(
            f"\n⚠️  ALERTA: Stock bajo para '{data['nombre']}'\n"
            f"   Stock actual: {data['stock']} | Mínimo: {data['stock_minimo']}\n"
        )
    
    def _alerta_producto_agotado(self, event: ProductoAgotadoEvent) -> None:
        """Generar alerta de producto agotado."""
        data = event.data
        print(
            f"\n🔴 CRÍTICO: Producto AGOTADO '{data['nombre']}'\n"
        )


class AuditoriaListener(Observer):
    """Observer que registra eventos en un log de auditoría."""
    
    def __init__(self):
        """Inicializar listener de auditoría."""
        self.auditlog = []
    
    def update(self, event: Event) -> None:
        """Registrar evento en auditoría."""
        log_entry = {
            'timestamp': event.timestamp,
            'evento': event.event_type,
            'datos': event.data,
        }
        self.auditlog.append(log_entry)
        print(f"[AUDIT] {event.event_type}: {event.data}")
    
    def obtener_auditoria(self, limite: int = 50):
        """Obtener últimos N eventos de auditoría."""
        return self.auditlog[-limite:]


class NotificacionesListener(Observer):
    """Observer que envía notificaciones."""
    
    def __init__(self):
        """Inicializar listener de notificaciones."""
        self.notificaciones = []
    
    def update(self, event: Event) -> None:
        """Enviar notificación basada en el evento."""
        if event.event_type == 'stock_bajo':
            self._notificar_stock_bajo(event)
        elif event.event_type == 'producto_agotado':
            self._notificar_producto_agotado(event)
        elif event.event_type == 'movimiento_registrado':
            self._notificar_movimiento(event)
    
    def _notificar_stock_bajo(self, event: Event) -> None:
        """Enviar notificación de stock bajo."""
        data = event.data
        notif = {
            'tipo': 'advertencia',
            'titulo': f"Stock bajo: {data['nombre']}",
            'mensaje': f"Stock actual: {data['stock']}, Mínimo: {data['stock_minimo']}",
            'timestamp': event.timestamp,
        }
        self.notificaciones.append(notif)
    
    def _notificar_producto_agotado(self, event: Event) -> None:
        """Enviar notificación de producto agotado."""
        data = event.data
        notif = {
            'tipo': 'error',
            'titulo': f"PRODUCTO AGOTADO: {data['nombre']}",
            'mensaje': 'Requiere reabastecimiento inmediato',
            'timestamp': event.timestamp,
        }
        self.notificaciones.append(notif)
    
    def _notificar_movimiento(self, event: Event) -> None:
        """Enviar notificación de movimiento registrado."""
        data = event.data
        notif = {
            'tipo': 'info',
            'titulo': f"Movimiento registrado: {data['tipo'].capitalize()}",
            'mensaje': f"Producto ID: {data['producto_id']}, Cantidad: {data['cantidad']}",
            'timestamp': event.timestamp,
        }
        self.notificaciones.append(notif)
    
    def obtener_notificaciones(self, limite: int = 10):
        """Obtener últimas N notificaciones."""
        return self.notificaciones[-limite:]
