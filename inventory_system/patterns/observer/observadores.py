"""
observer/observadores.py
========================
Observadores concretos.

Responsabilidad:
    - AlertaConsolaObservador: mostrar alertas de stock bajo
    - AlertaStockCriticoObservador: mostrar alertas de agotamiento
    - LogObservador: mantener historial de eventos
"""

from datetime import datetime
from typing import List
from models import Producto
from .interfaz import ObservadorStock


class AlertaConsolaObservador(ObservadorStock):
    """
    Observador que imprime alertas de stock bajo directamente en consola.
    Solo actúa cuando el stock del producto está por debajo del mínimo.
    """

    def actualizar(self, producto: Producto, evento: str, cantidad: int) -> None:
        if producto.stock_bajo:
            print(
                f"\n  ⚠  ALERTA DE STOCK BAJO"
                f"\n  Producto : {producto.nombre} (ID: {producto.id})"
                f"\n  Stock    : {producto.stock} unidades (mínimo: {producto.stock_minimo})"
                f"\n  Evento   : {evento.upper()} de {cantidad} unidades"
            )


class AlertaStockCriticoObservador(ObservadorStock):
    """
    Observador para nivel crítico: stock igual a 0.
    Informa que el producto está agotado.
    """

    def actualizar(self, producto: Producto, evento: str, cantidad: int) -> None:
        if producto.stock == 0:
            print(
                f"\n  🚨 STOCK AGOTADO"
                f"\n  Producto: {producto.nombre} (ID: {producto.id}) — sin unidades disponibles."
            )


class LogObservador(ObservadorStock):
    """
    Observador que mantiene un historial interno de eventos de stock.
    Los logs pueden consultarse en cualquier momento.
    """

    def __init__(self):
        self._logs: List[str] = []

    def actualizar(self, producto: Producto, evento: str, cantidad: int) -> None:
        entrada = (
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
            f"{evento.upper()} | Producto: '{producto.nombre}' (ID: {producto.id}) | "
            f"Cantidad: {cantidad} | Stock resultante: {producto.stock}"
        )
        self._logs.append(entrada)

    def mostrar_logs(self) -> None:
        """Imprime todos los eventos registrados."""
        if not self._logs:
            print("  No hay eventos registrados aún.")
            return
        print("\n  === HISTORIAL DE EVENTOS DE STOCK ===")
        for log in self._logs:
            print(f"  {log}")

    def obtener_logs(self) -> List[str]:
        return list(self._logs)
