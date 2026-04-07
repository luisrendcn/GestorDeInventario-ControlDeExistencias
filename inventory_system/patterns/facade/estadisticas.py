"""
facade/estadisticas.py
======================
Mixin: Historial, logs y estadísticas.

Responsabilidad:
    - Recuperar historial de transacciones
    - Mostrar logs de eventos
    - Calcular estadísticas del sistema
    - Listar tipos disponibles de productos
"""

from typing import Dict, Any, List


class EstadisticasMixin:
    """Mixin para historial, logs y estadísticas."""

    def historial_transacciones(self):
        """Retorna el historial completo de ventas y compras."""
        return self._transaccion_service.obtener_historial()

    def mostrar_logs(self) -> None:
        """Imprime el log de eventos de stock registrados por el observador."""
        self._log_observador.mostrar_logs()

    def estadisticas(self) -> Dict[str, Any]:
        """Retorna un resumen estadístico del inventario."""
        productos = self._inventario.listar_todos()
        transacciones = self._transaccion_service.obtener_historial()
        return {
            "total_productos": self._inventario.total_productos(),
            "valor_inventario": self._inventario.valor_total_inventario(),
            "productos_stock_bajo": len(self._inventario.productos_con_stock_bajo()),
            "total_transacciones": len(transacciones),
            "total_ventas": sum(1 for t in transacciones if t.tipo.value == "Venta"),
            "total_compras": sum(1 for t in transacciones if t.tipo.value == "Compra"),
            "ingresos_ventas": sum(t.total for t in transacciones if t.tipo.value == "Venta"),
            "costo_compras": sum(t.total for t in transacciones if t.tipo.value == "Compra"),
        }

    def tipos_producto_disponibles(self) -> List[str]:
        """Retorna los tipos de producto que pueden crearse."""
        from patterns.factory import FactoryManager
        return FactoryManager.tipos_disponibles()
