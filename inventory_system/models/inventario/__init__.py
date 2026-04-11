"""
inventario/
-----------
Módulo de inventario con máximo SRP (Single Responsibility Principle).

Estructura jerárquica de directorios y responsabilidades:

    inventario/
    ├── inventario.py          ⭐ ORQUESTADOR (solo coordina mixins)
    │
    ├── repositorio/           📦 Estructura de datos
    │   └── __init__.py        RepositorioMixin: _productos, _historial_movimientos, __len__, __repr__
    │
    ├── historial/             📋 Auditoría de movimientos
    │   ├── __init__.py        HistorialMixin
    │   ├── registrar_movimiento.py
    │   ├── obtener_historial.py
    │   └── limpiar_historial.py
    │
    ├── crud/                  🔧 Operaciones CRUD
    │   ├── __init__.py        CRUDMixin
    │   ├── agregar.py
    │   ├── obtener.py
    │   ├── obtener_o_error.py
    │   ├── eliminar.py
    │   ├── actualizar_stock_entrada.py
    │   ├── actualizar_stock_salida.py
    │   ├── obtener_stock_actual.py
    │   └── validar_stock_no_negativo.py
    │
    ├── busqueda/              🔍 Búsqueda y Listado
    │   ├── __init__.py        BúsquedaMixin
    │   ├── listar_todos.py
    │   └── buscar_por_nombre.py
    │
    └── consultas/             📊 Consultas y Análisis
        ├── __init__.py        ConsultasMixin
        ├── existe.py
        ├── total_productos.py
        ├── valor_total_inventario.py
        ├── productos_con_stock_bajo.py
        ├── productos_agotados.py
        ├── productos_disponibles.py
        ├── obtener_stock_total.py
        ├── obtener_reporte_stock.py
        ├── obtener_productos_mayor_stock.py
        └── obtener_productos_menor_stock.py

Responsabilidades desacopladas:

    ✅ Repositorio
        └─ Única responsabilidad: Mantener estructuras de datos (_productos, _historial)

    ✅ Historial
        └─ Única responsabilidad: Auditoría de movimientos (registrar, consultar, limpiar)

    ✅ CRUD
        └─ Única responsabilidad: Operaciones de creación, lectura, actualización, eliminación

    ✅ Búsqueda
        └─ Única responsabilidad: Búsqueda y listado de productos

    ✅ Consultas
        └─ Única responsabilidad: Análisis, filtros y reportes (lectura pura)

    ✅ Inventario (Orquestador)
        └─ Única responsabilidad: Coordinar la composición de todos los mixins

Uso:

    from models.inventario import Inventario
    
    inv = Inventario()
    inv.agregar(producto)           # CRUD
    inv.listar_todos()              # Búsqueda
    inv.obtener_reporte_stock()     # Consultas
    inv.obtener_historial()         # Historial
"""

from .inventario import Inventario

__all__ = ['Inventario']

