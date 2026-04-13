"""
╔════════════════════════════════════════════════════════════════════════════╗
║                  ARCHIVO: db.py (REFACTORIZADO)                           ║
║                  FUNCIÓN: Wrapper que orquesta la BD (FACADE)             ║
╚════════════════════════════════════════════════════════════════════════════╝

📋 CAMBIO ARQUITECTÓNICO:
   La clase original Database monolítica (500+ líneas, 5+ responsabilidades)
   ha sido refactorizada en módulos especializados bajo la carpeta `database/`

   ANTES: Una clase Database con 5 responsabilidades
   DESPUÉS: DatabaseManager FACADE orquestando 6 módulos especializados

🎯 ESTRUCTURA NUEVA (carpeta database/):
   ├── connection.py         → DatabaseConnection (gestión de conexión)
   ├── schema_creator.py     → SchemaCreator (creación de esquema)
   ├── product_operations.py → ProductOperations (CRUD de productos)
   ├── history_manager.py    → HistoryManager (historial de movimientos)
   ├── report_generator.py   → ReportGenerator (generación de reportes)
   ├── demo_manager.py       → DemoManager (datos de demostración)
   └── __init__.py           → DatabaseManager (FACADE)

✨ BENEFICIOS:
   ✓ Cada clase tiene UNA responsabilidad (SRP)
   ✓ Código más mantenible y testeable
   ✓ Fácil de extender sin afectar otros módulos
   ✓ Separación clara de concerns
   ✓ Compatible con código existente (mismo API)
"""

import os
from typing import List, Optional, Dict, Any
from database import DatabaseManager


# Instancia global (compatibilidad con código existente)
class Database:
    """
    Wrapper FACADE: mantiene compatibilidad con código existente
    mientras delega a la arquitectura modular en la carpeta database/
    """
    
    def __init__(self):
        """Inicializa el DatabaseManager modularizado."""
        db_path = os.getenv("DB_PATH", "control_existencias.db")
        self._manager = DatabaseManager(db_path)
    
    # ╔═══════════════════════════════════════════════════════════════╗
    # ║ Conexión (delegado a DatabaseConnection)                    ║
    # ╚═══════════════════════════════════════════════════════════════╝
    
    def conectar(self):
        """Conecta a la BD."""
        self._manager.conectar()
        self._manager.crear_tablas()
        print(f"[DB] Conectado a SQLite: {self._manager.ruta}")
    
    def desconectar(self):
        """Desconecta de la BD."""
        self._manager.cerrar()
        print("[DB] Desconectado")
    
    def cerrar(self):
        """Alias para desconectar()."""
        self.desconectar()
    
    # ╔═══════════════════════════════════════════════════════════════╗
    # ║ Operaciones de Productos (delegado a ProductOperations)     ║
    # ╚═══════════════════════════════════════════════════════════════╝
    
    def crear_producto(self, producto) -> bool:
        """Crea un producto."""
        try:
            self._manager.crear_producto(
                nombre=producto.nombre,
                precio=producto.precio,
                stock=getattr(producto, 'stock', 0),
                stock_minimo=getattr(producto, 'stock_minimo', 0)
            )
            return True
        except Exception as e:
            raise Exception(f"Error creando producto: {e}")
    
    def obtener_producto(self, producto_id: str) -> Optional[Dict]:
        """Obtiene un producto por ID."""
        return self._manager.obtener_producto(producto_id)
    
    def listar_productos(self) -> List[Dict]:
        """Lista todos los productos."""
        return self._manager.listar_productos()
    
    def actualizar_stock(self, producto_id: str, nuevo_stock: int, 
                        tipo: str = "", cantidad: int = 0, motivo: str = "") -> bool:
        """Actualiza stock de un producto."""
        self._manager.actualizar_stock(producto_id, nuevo_stock)
        if tipo:
            self._manager.registrar_movimiento(producto_id, tipo, cantidad, motivo)
        return True
    
    def eliminar_producto(self, producto_id: str) -> bool:
        """Elimina un producto."""
        self._manager.eliminar_producto(producto_id)
        return True
    
    # ╔═══════════════════════════════════════════════════════════════╗
    # ║ Historial (delegado a HistoryManager)                       ║
    # ╚═══════════════════════════════════════════════════════════════╝
    
    def obtener_historial(self, producto_id: Optional[str] = None, 
                         limite: int = 100) -> List[Dict]:
        """Obtiene historial de movimientos."""
        return self._manager.obtener_historial(producto_id)
    
    def registrar_movimiento(self, producto_id: str, tipo: str, cantidad: int,
                            descripcion: str = "") -> None:
        """Registra un movimiento."""
        self._manager.registrar_movimiento(producto_id, tipo, cantidad, descripcion)
    
    # ╔═══════════════════════════════════════════════════════════════╗
    # ║ Reportes (delegado a ReportGenerator)                       ║
    # ╚═══════════════════════════════════════════════════════════════╝
    
    def obtener_reporte(self) -> Dict[str, Any]:
        """Genera reporte de existencias."""
        return self._manager.obtener_reporte()
    
    # ╔═══════════════════════════════════════════════════════════════╗
    # ║ Demo (delegado a DemoManager)                               ║
    # ╚═══════════════════════════════════════════════════════════════╝
    
    def inicializar_datos_demo(self) -> List[Dict]:
        """Inicializa datos de demostración."""
        self._manager.inicializar_datos_demo()
        print(f"[DB] ✅ Datos de demostración inicializados")
        return self.listar_productos()
    
    def limpiar_base_datos(self) -> bool:
        """Limpia la base de datos."""
        self._manager.limpiar_base_datos()
        print("[DB] ✅ Base de datos limpiada")
        return True


# Instancia global (compatibilidad)
db = Database()
