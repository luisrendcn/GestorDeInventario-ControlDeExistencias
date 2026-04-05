"""
patterns/observer.py
--------------------
PATRÓN COMPORTAMENTAL: Observer (Observador)

Problema resuelto:
    Cuando el stock de un producto cambia, varios subsistemas necesitan
    reaccionar (mostrar alertas, escribir logs, etc.) sin que el objeto
    central conozca esos subsistemas directamente.

Participantes:
    - ObservadorStock (interfaz abstracta): contrato para los observadores
    - SujetoStock: el publicador que notifica cambios
    - AlertaConsolaObservador: muestra alertas en pantalla
    - LogObservador: escribe un registro de eventos
    - AlertaStockCriticoObservador: alerta diferenciada para nivel crítico
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import List
from models.producto import Producto


# ---------------------------------------------------------------------------
# Interfaz del Observador
# ---------------------------------------------------------------------------

class ObservadorStock(ABC):
    """Interfaz abstracta que deben implementar todos los observadores."""

    @abstractmethod
    def actualizar(self, producto: Producto, evento: str, cantidad: int) -> None:
        """
        Llamado cuando ocurre un evento de stock.

        Args:
            producto: El producto afectado.
            evento: Descripción del evento ('venta', 'compra', 'edicion').
            cantidad: Cantidad involucrada en el movimiento.
        """
        pass


# ---------------------------------------------------------------------------
# Sujeto (Publicador)
# ---------------------------------------------------------------------------

class SujetoStock:
    """
    Publicador que mantiene la lista de observadores y los notifica.
    Aplica bajo acoplamiento: no conoce los detalles de cada observador.
    """

    def __init__(self):
        self._observadores: List[ObservadorStock] = []

    def suscribir(self, observador: ObservadorStock) -> None:
        """Registra un nuevo observador."""
        if observador not in self._observadores:
            self._observadores.append(observador)

    def desuscribir(self, observador: ObservadorStock) -> None:
        """Elimina un observador registrado."""
        self._observadores.remove(observador)

    def notificar(self, producto: Producto, evento: str, cantidad: int) -> None:
        """Notifica a todos los observadores sobre un evento de stock."""
        for observador in self._observadores:
            observador.actualizar(producto, evento, cantidad)


# ---------------------------------------------------------------------------
# Observadores concretos
# ---------------------------------------------------------------------------

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
