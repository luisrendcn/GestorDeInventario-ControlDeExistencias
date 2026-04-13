"""
╔════════════════════════════════════════════════════════════════════════════╗
║           ARCHIVO: services/service_container.py                          ║
║           FUNCIÓN: Contenedor de inyección de dependencias                ║
╚════════════════════════════════════════════════════════════════════════════╝

📋 RESPONSABILIDAD DEL ARCHIVO (1):
   Instanciar y proporcionar acceso a TODOS los servicios atómicos

═════════════════════════════════════════════════════════════════════════════

🏛️ PATRÓN: SERVICE LOCATOR + DEPENDENCY INJECTION CONTAINER
   
   En lugar de que cada endpoint cree sus propios servicios,
   el contenedor los crea UNA SOLA VEZ (singleton) y los distribuye.
   
   Ventajas:
   • Una única instancia de cada servicio
   • Fácil de testear (mockear el contenedor)
   • Desacoplamiento entre endpoints y servicios
   • Punto central de configuración

🎯 CONTENEDOR PROPORCIONA:

   SERVICIOS DE PRODUCTOS (6):
   ├─ CrearProductoService
   ├─ ObtenerProductoService
   ├─ ListarProductosService
   ├─ ActualizarProductoService
   ├─ EliminarProductoService
   └─ BuscarProductoService
   
   ESTRATEGIAS DE INVENTARIO (3):
   ├─ EntradaStrategy
   ├─ SalidaStrategy
   └─ AjusteStrategy
   
   SERVICIOS DE REPORTE (6):
   ├─ ReporteGeneralService
   ├─ AlertasService
   ├─ HistorialService
   ├─ ProductosMayorStockService
   ├─ ProductosMenorStockService
   └─ ValuationService
"""

from services.producto_services import (
    CrearProductoService,
    ObtenerProductoService,
    ListarProductosService,
    ActualizarProductoService,
    EliminarProductoService,
    BuscarProductoService,
)

from services.inventario_strategies import (
    EntradaStrategy,
    SalidaStrategy,
    AjusteStrategy,
)

from services.reporte_services import (
    ReporteGeneralService,
    AlertasService,
    HistorialService,
    ProductosMayorStockService,
    ProductosMenorStockService,
    ValuationService,
)

from infrastructure.repositories import (
    RepositorioFactory,
    MovimientoRepositoryFactory,
)


class ServiceContainer:
    """
    Contenedor centralizado de inyección de dependencias.
    
    RESPONSABILIDAD (1):
      1️⃣  Instanciar y proporcionar acceso a todos los servicios
    
    Patrón: SERVICE LOCATOR (singleton en la aplicación)
    
    Uso:
        container = ServiceContainer()
        crear_svc = container.get_crear_producto_service()
        listar_svc = container.get_listar_productos_service()
        entrada_strategy = container.get_entrada_strategy()
        reporte_svc = container.get_reporte_general_service()
    """
    
    # Singleton instances (lazy initialization)
    _producto_repo = None
    _movimiento_repo = None
    
    # Servicios de Producto
    _crear_producto_service = None
    _obtener_producto_service = None
    _listar_productos_service = None
    _actualizar_producto_service = None
    _eliminar_producto_service = None
    _buscar_producto_service = None
    
    # Estrategias de Inventario
    _entrada_strategy = None
    _salida_strategy = None
    _ajuste_strategy = None
    
    # Servicios de Reporte
    _reporte_general_service = None
    _alertas_service = None
    _historial_service = None
    _productos_mayor_stock_service = None
    _productos_menor_stock_service = None
    _valuation_service = None
    
    # ═══════════════════════════════════════════════════════════════════════
    # REPOSITORIOS (inyectados en los servicios)
    # ═══════════════════════════════════════════════════════════════════════
    
    @classmethod
    def get_producto_repository(cls):
        """Obtener repositorio de productos (singleton)."""
        if cls._producto_repo is None:
            cls._producto_repo = RepositorioFactory.get_producto_repository()
        return cls._producto_repo
    
    @classmethod
    def get_movimiento_repository(cls):
        """Obtener repositorio de movimientos (singleton)."""
        if cls._movimiento_repo is None:
            cls._movimiento_repo = MovimientoRepositoryFactory.get_movimiento_repository()
        return cls._movimiento_repo
    
    # ═══════════════════════════════════════════════════════════════════════
    # SERVICIOS DE PRODUCTO (6 servicios atómicos)
    # ═══════════════════════════════════════════════════════════════════════
    
    @classmethod
    def get_crear_producto_service(cls) -> CrearProductoService:
        """Obtener servicio de creación de productos."""
        if cls._crear_producto_service is None:
            cls._crear_producto_service = CrearProductoService(
                cls.get_producto_repository()
            )
        return cls._crear_producto_service
    
    @classmethod
    def get_obtener_producto_service(cls) -> ObtenerProductoService:
        """Obtener servicio de obtención de un producto."""
        if cls._obtener_producto_service is None:
            cls._obtener_producto_service = ObtenerProductoService(
                cls.get_producto_repository()
            )
        return cls._obtener_producto_service
    
    @classmethod
    def get_listar_productos_service(cls) -> ListarProductosService:
        """Obtener servicio de listado de productos."""
        if cls._listar_productos_service is None:
            cls._listar_productos_service = ListarProductosService(
                cls.get_producto_repository()
            )
        return cls._listar_productos_service
    
    @classmethod
    def get_actualizar_producto_service(cls) -> ActualizarProductoService:
        """Obtener servicio de actualización de productos."""
        if cls._actualizar_producto_service is None:
            cls._actualizar_producto_service = ActualizarProductoService(
                cls.get_producto_repository()
            )
        return cls._actualizar_producto_service
    
    @classmethod
    def get_eliminar_producto_service(cls) -> EliminarProductoService:
        """Obtener servicio de eliminación de productos."""
        if cls._eliminar_producto_service is None:
            cls._eliminar_producto_service = EliminarProductoService(
                cls.get_producto_repository()
            )
        return cls._eliminar_producto_service
    
    @classmethod
    def get_buscar_producto_service(cls) -> BuscarProductoService:
        """Obtener servicio de búsqueda de productos."""
        if cls._buscar_producto_service is None:
            cls._buscar_producto_service = BuscarProductoService(
                cls.get_producto_repository()
            )
        return cls._buscar_producto_service
    
    # ═══════════════════════════════════════════════════════════════════════
    # ESTRATEGIAS DE INVENTARIO (3 estrategias de movimiento)
    # ═══════════════════════════════════════════════════════════════════════
    
    @classmethod
    def get_entrada_strategy(cls) -> EntradaStrategy:
        """Obtener estrategia de entrada de stock."""
        if cls._entrada_strategy is None:
            cls._entrada_strategy = EntradaStrategy(
                cls.get_producto_repository(),
                cls.get_movimiento_repository()
            )
        return cls._entrada_strategy
    
    @classmethod
    def get_salida_strategy(cls) -> SalidaStrategy:
        """Obtener estrategia de salida de stock."""
        if cls._salida_strategy is None:
            cls._salida_strategy = SalidaStrategy(
                cls.get_producto_repository(),
                cls.get_movimiento_repository()
            )
        return cls._salida_strategy
    
    @classmethod
    def get_ajuste_strategy(cls) -> AjusteStrategy:
        """Obtener estrategia de ajuste de stock."""
        if cls._ajuste_strategy is None:
            cls._ajuste_strategy = AjusteStrategy(
                cls.get_producto_repository(),
                cls.get_movimiento_repository()
            )
        return cls._ajuste_strategy
    
    # ═══════════════════════════════════════════════════════════════════════
    # SERVICIOS DE REPORTE (6 servicios de reportes)
    # ═══════════════════════════════════════════════════════════════════════
    
    @classmethod
    def get_reporte_general_service(cls) -> ReporteGeneralService:
        """Obtener servicio de reporte general."""
        if cls._reporte_general_service is None:
            cls._reporte_general_service = ReporteGeneralService(
                cls.get_producto_repository()
            )
        return cls._reporte_general_service
    
    @classmethod
    def get_alertas_service(cls) -> AlertasService:
        """Obtener servicio de alertas."""
        if cls._alertas_service is None:
            cls._alertas_service = AlertasService(
                cls.get_producto_repository()
            )
        return cls._alertas_service
    
    @classmethod
    def get_historial_service(cls) -> HistorialService:
        """Obtener servicio de historial."""
        if cls._historial_service is None:
            cls._historial_service = HistorialService(
                cls.get_producto_repository(),
                cls.get_movimiento_repository()
            )
        return cls._historial_service
    
    @classmethod
    def get_productos_mayor_stock_service(cls) -> ProductosMayorStockService:
        """Obtener servicio de productos con mayor stock."""
        if cls._productos_mayor_stock_service is None:
            cls._productos_mayor_stock_service = ProductosMayorStockService(
                cls.get_producto_repository()
            )
        return cls._productos_mayor_stock_service
    
    @classmethod
    def get_productos_menor_stock_service(cls) -> ProductosMenorStockService:
        """Obtener servicio de productos con menor stock."""
        if cls._productos_menor_stock_service is None:
            cls._productos_menor_stock_service = ProductosMenorStockService(
                cls.get_producto_repository()
            )
        return cls._productos_menor_stock_service
    
    @classmethod
    def get_valuation_service(cls) -> ValuationService:
        """Obtener servicio de valuación."""
        if cls._valuation_service is None:
            cls._valuation_service = ValuationService(
                cls.get_producto_repository()
            )
        return cls._valuation_service
