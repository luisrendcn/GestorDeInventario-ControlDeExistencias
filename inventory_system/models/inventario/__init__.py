"""
inventario/
-----------
Módulo de repositorio de inventario con máximo desacoplamiento.

Arquitectura de Máximo SRP (Single Responsibility Principle):
    
    Estructura por directorios:
    └── inventario/
        ├── __init__.py
        ├── inventario.py              (Clase coordinadora principal)
        ├── crud/                       (Operaciones CRUD)
        │   ├── __init__.py            (Exporta CRUDMixin)
        │   ├── agregar.py             (AgregarMixin)
        │   ├── obtener.py             (ObtenerMixin)
        │   ├── obtener_o_error.py     (ObtenerOErrorMixin)
        │   ├── eliminar.py            (EliminarMixin)
        │   ├── actualizar_stock_entrada.py
        │   ├── actualizar_stock_salida.py
        │   ├── obtener_stock_actual.py
        │   └── validar_stock_no_negativo.py
        │
        ├── busqueda/                  (Búsqueda y listado)
        │   ├── __init__.py            (Exporta BúsquedaMixin)
        │   ├── listar_todos.py        (ListarTodosMixin)
        │   └── buscar_por_nombre.py   (BuscarPorNombreMixin)
        │
        └── consultas/                 (Consultas y análisis)
            ├── __init__.py            (Exporta ConsultasMixin)
            ├── existe.py              (ExisteMixin)
            ├── total_productos.py     (TotalProductosMixin)
            ├── valor_total_inventario.py
            ├── productos_con_stock_bajo.py
            ├── productos_agotados.py
            ├── productos_disponibles.py
            ├── obtener_stock_total.py
            ├── obtener_reporte_stock.py
            ├── obtener_productos_mayor_stock.py
            └── obtener_productos_menor_stock.py

Principios Aplicados:
    ✅ SRP: Un archivo = Una responsabilidad
    ✅ Cohesión: Métodos relacionados aunque separados
    ✅ Bajo acoplamiento: Cada mixin es independiente
    ✅ Composición: CRUDMixin, BúsquedaMixin, ConsultasMixin heredan de sub-mixins
    ✅ Jerarquía clara: Directorios → Funcionalidad → Método

Uso:
    from models.inventario import Inventario
    
    inv = Inventario()
    inv.agregar(producto)        # CRUD
    inv.listar_todos()            # Búsqueda
    inv.obtener_reporte_stock()  # Consultas
"""

from .inventario import Inventario

__all__ = ['Inventario']
