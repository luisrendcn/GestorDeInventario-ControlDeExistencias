"""
╔════════════════════════════════════════════════════════════════════════════╗
║                         CAPA: INFRASTRUCTURE                              ║
║                                                                            ║
║           Servicios de acceso a datos y base de datos                     ║
╚════════════════════════════════════════════════════════════════════════════╝

📦 COMPONENTES PRINCIPALES:

┌─ database/                   (Servicios atómicos de BD)
│  ├─ 🔌 ConnectionManager  - Gestionar ciclo de vida de conexión SQLite
│  ├─ 🔧 SchemaInitializer  - Crear e inicializar tablas
│  ├─ ✏️  QueryExecutor     - Ejecutar queries de modificación (INSERT/UPDATE/DELETE)
│  ├─ 🔍 QueryReader       - Ejecutar queries de lectura (SELECT)
│  ├─ 🧹 DatabaseCleaner   - Limpiar/resetear BD (desarrollo/testing)
│  └─ 📦 Database          - Facade para acceso conveniente a todos los servicios
│
└─ repositories/               (Patrones de acceso a datos)
   ├─ 🏪 ProductoRepository      - CRUD de Productos (crear, obtener, listar, eliminar, actualizar)
   ├─ 📊 MovimientoRepository    - Historial de movimientos (registrar, obtener_historial, limpiar)
   ├─ 🔐 DatabaseStore          - Almacena conexión BD global (Singleton)
   ├─ 🏭 RepositorioFactory      - Factory para ProductoRepository
   └─ 🏭 MovimientoRepositoryFactory - Factory para MovimientoRepository

═════════════════════════════════════════════════════════════════════════════

📊 ESTRUCTURA DETALLADA:

DATABASE (Servicios atómicos):
├─ connection_manager/
│  ├─ conectar.py      (ConectarMixin)
│  ├─ desconectar.py   (DesconectarMixin - incluye alias cerrar())
│  └─ __init__.py      (ConnectionManager - orchestrator)
├─ schema_initializer/
│  ├─ crear_tablas.py  (CrearTablasMixin)
│  └─ __init__.py      (SchemaInitializer - orchestrator)
├─ query_executor/
│  ├─ ejecutar.py      (EjecutarMixin)
│  └─ __init__.py      (QueryExecutor - orchestrator)
├─ query_reader/
│  ├─ fetchone.py      (FetchoneMixin)
│  ├─ fetchall.py      (FetchallMixin)
│  └─ __init__.py      (QueryReader - orchestrator)
├─ database_cleaner/
│  ├─ limpiar_base_datos.py (LimpiarBaseDatosMixin)
│  └─ __init__.py      (DatabaseCleaner - orchestrator)
├─ database_facade.py  (Database - Facade pattern)
└─ __init__.py         (agregador)

REPOSITORIES (Patrones de acceso):
├─ producto_repository/
│  ├─ crear.py         (CrearMixin)
│  ├─ obtener.py       (ObtenerMixin)
│  ├─ listar.py        (ListarMixin)
│  ├─ eliminar.py      (EliminarMixin)
│  ├─ actualizar.py    (ActualizarMixin)
│  └─ __init__.py      (ProductoRepository - orchestrator)
├─ movimiento_repository/
│  ├─ registrar_movimiento.py (RegistrarMovimientoMixin)
│  ├─ obtener_historial.py    (ObtenerHistorialMixin)
│  ├─ limpiar_historial.py    (LimpiarHistorialMixin)
│  └─ __init__.py      (MovimientoRepository - orchestrator)
├─ database_store/
│  ├─ set_database.py  (SetDatabaseMixin)
│  ├─ get_database.py  (GetDatabaseMixin)
│  └─ __init__.py      (DatabaseStore - Singleton)
├─ repositorio_factory/
│  ├─ get_producto_repository.py (GetProductoRepositoryMixin)
│  └─ __init__.py      (RepositorioFactory - orchestrator)
├─ movimiento_repository_factory/
│  ├─ get_movimiento_repository.py (GetMovimientoRepositoryMixin)
│  └─ __init__.py      (MovimientoRepositoryFactory - orchestrator)
└─ __init__.py         (agregador)

═════════════════════════════════════════════════════════════════════════════

🏛️ PATRONES IMPLEMENTADOS:

✅ SINGLE RESPONSIBILITY PRINCIPLE (SRP)
   • Cada archivo: 1 responsabilidad
   • ProductoRepository: CRUD de Productos (5 archivos + orchestrator)
   • MovimientoRepository: Historial (3 archivos + orchestrator)
   • DatabaseStore: Singleton (2 archivos + orchestrator)
   • Factories: Creación de repositorios (1 archivo cada una + orchestrator)

✅ COMPOSITION VÍA MIXINS (3-Level Hierarchy)
   Level 1: Atomic mixins (1 método per archivo)
   Level 2: Orchestrators (combinan múltiples submixins via herencia)
   Level 3: Main classes (heredan de orchestrators)

✅ REPOSITORY PATTERN
   • Abstracción de acceso a datos
   • Domain Models NO conocen detalles de BD
   • Repositories adaptan Domain ↔ Persistence

✅ FACTORY METHOD PATTERN
   • RepositorioFactory: creación centralizada de ProductoRepository
   • MovimientoRepositoryFactory: creación centralizada
   • Singleton + Lazy initialization

✅ SINGLETON PATTERN
   • DatabaseStore: una única instancia de conexión global
   • Factories: una única instancia de cada repositorio

═════════════════════════════════════════════════════════════════════════════

📝 EJEMPLOS DE USO:

# 1. Opción: Database Facade (recomendado para app.py)
from infrastructure.database import Database
db = Database('inventario.db')
db.conectar()
db.crear_tablas()

# 2. Opción: Servicios individuales
from infrastructure.database import ConnectionManager, QueryExecutor
conn_manager = ConnectionManager('inventario.db')
conn_manager.conectar()
executor = QueryExecutor(conn_manager.conn)
executor.ejecutar('INSERT INTO ...', (...))

# 3. Opción: Repositories + Factories
from infrastructure.repositories import (
    DatabaseStore, RepositorioFactory, MovimientoRepositoryFactory
)
DatabaseStore.set_database(db.conn)
producto_repo = RepositorioFactory.get_producto_repository()
movimiento_repo = MovimientoRepositoryFactory.get_movimiento_repository()
productos = producto_repo.listar()

═════════════════════════════════════════════════════════════════════════════

🎓 ARCHÍTECTURA LIMPIA:

Domain (core/)
    ↑
Services (services/)
    ↑
API (api/)
    ↑
INFRASTRUCTURE (esta capa)
    ├─ database/     (Servicios BD atómicos)
    └─ repositories/ (Patrones de acceso)

Domain Models NO dependen de detalles de BD.
Repositories adaptan Domain ↔ Persistence.
Services usan Repositories para acceso a datos.
API orquesta servicios y devuelve respuestas.

═════════════════════════════════════════════════════════════════════════════
"""

from .database import Database
from .repositories import ProductoRepository

__all__ = ['Database', 'ProductoRepository']
