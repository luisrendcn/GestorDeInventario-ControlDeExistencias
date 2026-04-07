"""
facade/facade.py
================
Coordinador: Fachada del sistema de inventario.

Responsabilidad:
    - Centralizar toda la interfaz del sistema
    - Coordinar los subsistemas internos
    - Inicializar y configurar los observadores
    - Heredar de 3 mixins para organizar métodos por responsabilidad

Subsistemas coordinados:
    - Inventario (repositorio de productos)
    - InventarioService (lógica de negocio de stock)
    - TransaccionService (registro de ventas/compras)
    - SujetoStock + observadores (notificaciones)
    - FactoryManager (creación de productos)
"""

from models import Inventario
from services.inventario_service import InventarioService
from services.transaccion_service import TransaccionService
from patterns.observer import (
    SujetoStock,
    AlertaConsolaObservador,
    AlertaStockCriticoObservador,
    LogObservador,
)
from .producto_management import ProductoManagementMixin
from .transacciones import TransaccionesMixin
from .estadisticas import EstadisticasMixin


class SistemaInventarioFacade(
    ProductoManagementMixin, TransaccionesMixin, EstadisticasMixin
):
    """
    Fachada del sistema de inventario.

    Unifica en una sola interfaz todas las operaciones disponibles:
    - Gestión de productos (crear, editar, eliminar, listar)
    - Ventas y compras (con actualización de stock)
    - Notificaciones automáticas (a través del patrón Observer)
    - Consulta del historial de transacciones y logs

    Los controladores y la CLI SOLO interactúan con esta clase.
    """

    def __init__(self):
        # Subsistemas internos
        self._inventario = Inventario()
        self._transaccion_service = TransaccionService()

        # Configurar observadores
        self._sujeto = SujetoStock()
        self._log_observador = LogObservador()
        self._alerta_observador = AlertaConsolaObservador()
        self._alerta_critica_observador = AlertaStockCriticoObservador()

        self._sujeto.suscribir(self._log_observador)
        self._sujeto.suscribir(self._alerta_observador)
        self._sujeto.suscribir(self._alerta_critica_observador)

        # Servicio de inventario con acceso al sujeto para notificaciones
        self._inventario_service = InventarioService(
            self._inventario, self._sujeto
        )
