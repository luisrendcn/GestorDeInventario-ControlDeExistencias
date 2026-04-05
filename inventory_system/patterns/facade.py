"""
patterns/facade.py
------------------
PATRÓN ESTRUCTURAL: Facade (Fachada)

Problema resuelto:
    El sistema tiene múltiples subsistemas (inventario, servicios de venta,
    compra, notificaciones). El Facade expone una interfaz unificada y simple
    para que el controlador (CLI) no deba conocer ni coordinar
    manualmente cada subsistema.

Participantes:
    - SistemaInventarioFacade: clase fachada principal
      Internamente coordina:
        - Inventario (repositorio)
        - InventarioService (lógica de negocio)
        - TransaccionService (ventas/compras)
        - SujetoStock + observadores (notificaciones)
        - FactoryManager (creación de productos)
"""

from typing import Dict, Any, List, Optional
from models.inventario import Inventario
from models.producto import Producto
from models.transaccion import Transaccion
from services.inventario_service import InventarioService
from services.transaccion_service import TransaccionService
from patterns.observer import SujetoStock, AlertaConsolaObservador, AlertaStockCriticoObservador, LogObservador
from patterns.factory import FactoryManager


class SistemaInventarioFacade:
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
        self._inventario_service = InventarioService(self._inventario, self._sujeto)

    # -----------------------------------------------------------------------
    # Gestión de productos
    # -----------------------------------------------------------------------

    def crear_producto(self, tipo: str, datos: Dict[str, Any]) -> Producto:
        """
        Crea un producto usando el Factory Method y lo agrega al inventario.
        """
        producto = FactoryManager.crear_producto(tipo, datos)
        self._inventario_service.agregar_producto(producto)
        return producto

    def editar_producto(self, id: str, nuevos_datos: Dict[str, Any]) -> Producto:
        """Actualiza los campos editables de un producto existente."""
        return self._inventario_service.editar_producto(id, nuevos_datos)

    def eliminar_producto(self, id: str) -> Producto:
        """Elimina un producto del inventario."""
        return self._inventario_service.eliminar_producto(id)

    def obtener_producto(self, id: str) -> Optional[Producto]:
        """Retorna un producto por su ID."""
        return self._inventario.obtener(id)

    def listar_productos(self) -> List[Producto]:
        """Lista todos los productos del inventario."""
        return self._inventario.listar_todos()

    def buscar_productos(self, nombre: str) -> List[Producto]:
        """Búsqueda por nombre parcial."""
        return self._inventario.buscar_por_nombre(nombre)

    def productos_stock_bajo(self) -> List[Producto]:
        """Retorna productos con stock por debajo del mínimo."""
        return self._inventario.productos_con_stock_bajo()

    # -----------------------------------------------------------------------
    # Ventas y Compras
    # -----------------------------------------------------------------------

    def registrar_venta(self, producto_id: str, cantidad: int) -> Transaccion:
        """
        Registra una venta: reduce stock del producto y crea transacción.
        Notifica a los observadores tras el cambio.
        """
        return self._inventario_service.registrar_venta(
            producto_id, cantidad, self._transaccion_service
        )

    def registrar_compra(self, producto_id: str, cantidad: int, precio_unitario: Optional[float] = None) -> Transaccion:
        """
        Registra una compra: aumenta stock del producto y crea transacción.
        Notifica a los observadores tras el cambio.
        """
        return self._inventario_service.registrar_compra(
            producto_id, cantidad, self._transaccion_service, precio_unitario
        )

    # -----------------------------------------------------------------------
    # Historial y estadísticas
    # -----------------------------------------------------------------------

    def historial_transacciones(self) -> List[Transaccion]:
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
        return FactoryManager.tipos_disponibles()
