"""
observer/observer.py
====================
Coordinador: Sujeto (Publicador) que notifica a observadores.

Responsabilidad:
    - Mantener registro de observadores
    - Notificar a todos los observadores cuando ocurre un evento
    - Permitir suscripción y desuscripción
"""

from typing import List
from models import Producto
from .interfaz import ObservadorStock


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
