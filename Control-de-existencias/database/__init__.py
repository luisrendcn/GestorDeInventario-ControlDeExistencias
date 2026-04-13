"""
╔════════════════════════════════════════════════════════════════╗
║  ARCHIVO: database/__init__.py                                ║
║  FUNCIÓN: FACADE que orquesta todos los componentes           ║
╚════════════════════════════════════════════════════════════════╝

Patrón: FACADE
Responsabilidad: Coordinar todos los módulos de base de datos
"""

import sqlite3
from typing import Any, Dict, List
from .connection import DatabaseConnection
from .schema_creator import SchemaCreator
from .product_operations import ProductOperations
from .history_manager import HistoryManager
from .report_generator import ReportGenerator
from .demo_manager import DemoManager


class DatabaseManager:
    """
    FACADE que orquesta todos los componentes de base de datos.
    
    Patrón FACADE:
      • Proporciona interfaz unificada
      • Oculta complejidad de múltiples módulos
      • Mantiene compatibilidad con código existente
    
    Componentes orchestrados:
      1. DatabaseConnection - Gestión de conexión
      2. SchemaCreator - Creación de esquema
      3. ProductOperations - Operaciones CRUD de productos
      4. HistoryManager - Gestión de historial
      5. ReportGenerator - Generación de reportes
      6. DemoManager - Datos de demostración
    """
    
    def __init__(self, ruta_base_datos: str = "mi_base_datos.db"):
        """Inicializar facade con ruta de la BD."""
        self.ruta = ruta_base_datos
        self.connection = DatabaseConnection(ruta_base_datos)
        self.schema_creator = None
        self.product_ops = None
        self.history_manager = None
        self.report_generator = None
        self.demo_manager = None
        self.conn = None
    
    def conectar(self) -> None:
        """Conectar a la BD e inicializar todos los componentes."""
        self.conn = self.connection.conectar()
        self.schema_creator = SchemaCreator(self.conn)
        self.product_ops = ProductOperations(self.conn)
        self.history_manager = HistoryManager(self.conn)
        self.report_generator = ReportGenerator(self.conn)
        self.demo_manager = DemoManager(self.conn)
    
    def crear_tablas(self) -> None:
        """Crear esquema de BD."""
        if not self.schema_creator:
            raise RuntimeError("DatabaseManager no ha sido conectado")
        self.schema_creator.crear_tablas()
    
    def cerrar(self) -> None:
        """Cerrar conexión a la BD."""
        if self.connection:
            self.connection.cerrar()
    
    # ╔══════════════════════════════════════╗
    # ║ Delegación: Operaciones de Productos ║
    # ╚══════════════════════════════════════╝
    
    def crear_producto(self, nombre: str, precio: float, stock: int = 0, 
                      stock_minimo: int = 0) -> int:
        """Crear nuevo producto."""
        return self.product_ops.crear_producto(nombre, precio, stock, stock_minimo)
    
    def obtener_producto(self, producto_id: int) -> Dict[str, Any]:
        """Obtener producto por ID."""
        return self.product_ops.obtener_producto(producto_id)
    
    def listar_productos(self) -> List[Dict[str, Any]]:
        """Listar todos los productos."""
        return self.product_ops.listar_productos()
    
    def actualizar_stock(self, producto_id: int, cantidad: int) -> None:
        """Actualizar stock de producto."""
        self.product_ops.actualizar_stock(producto_id, cantidad)
    
    def eliminar_producto(self, producto_id: int) -> None:
        """Eliminar producto."""
        self.product_ops.eliminar_producto(producto_id)
    
    # ╔═══════════════════════════════════════╗
    # ║ Delegación: Gestión de Movimientos   ║
    # ╚═══════════════════════════════════════╝
    
    def registrar_movimiento(self, producto_id: int, tipo: str, cantidad: int,
                            descripcion: str = "") -> None:
        """Registrar movimiento de efectivo."""
        self.history_manager.registrar_movimiento(producto_id, tipo, cantidad, descripcion)
    
    def obtener_historial(self, producto_id: int = None) -> List[Dict[str, Any]]:
        """Obtener historial de movimientos."""
        return self.history_manager.obtener_historial(producto_id)
    
    # ╔═══════════════════════════════════════╗
    # ║ Delegación: Reportes                 ║
    # ╚═══════════════════════════════════════╝
    
    def obtener_reporte(self) -> Dict[str, Any]:
        """Obtener reporte de existencias."""
        return self.report_generator.obtener_reporte()
    
    def obtener_alertas(self) -> Dict[str, Any]:
        """Obtener alertas de inventario."""
        return self.report_generator.obtener_alertas()
    
    # ╔═══════════════════════════════════════╗
    # ║ Delegación: Demostración            ║
    # ╚═══════════════════════════════════════╝
    
    def inicializar_datos_demo(self) -> Dict[str, Any]:
        """Inicializar datos de demostración."""
        return self.demo_manager.inicializar_datos_demo()
    
    def limpiar_base_datos(self) -> Dict[str, Any]:
        """Limpiar base de datos."""
        return self.demo_manager.limpiar_base_datos()
    
    # ╔═══════════════════════════════════════╗
    # ║ Context Manager (with statement)     ║
    # ╚═══════════════════════════════════════╝
    
    def __enter__(self):
        """Soporte para: with DatabaseManager() as db:"""
        self.conectar()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Cerrar conexión al salir del context."""
        self.cerrar()
        return False


# Export principal para facilitar importación
__all__ = ["DatabaseManager"]
