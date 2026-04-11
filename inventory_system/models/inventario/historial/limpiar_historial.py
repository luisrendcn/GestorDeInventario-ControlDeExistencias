"""
historial/limpiar_historial.py
===============================
Operación: Limpiar historial de movimientos.

Responsabilidad única:
    - Vaciar todos los registros de auditoría
"""


class LimpiarHistorialMixin:
    """Mixin especializado en limpiar historial."""

    def limpiar_historial(self) -> None:
        """
        Limpia completamente el historial de movimientos.
        
        ⚠️ ADVERTENCIA: Esta operación es irreversible.
        Elimina todos los registros de auditoría del inventario.
        """
        self._historial_movimientos.clear()
