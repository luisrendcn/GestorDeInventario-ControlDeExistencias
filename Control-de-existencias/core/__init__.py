"""
╔════════════════════════════════════════════════════════════════════════════╗
║                    MÓDULO: core/                                          ║
║                    RESPONSABILIDAD: Punto de entrada del dominio          ║
╚════════════════════════════════════════════════════════════════════════════╝

🎯 ÚNICA RESPONSABILIDAD:
   Exportar y coordinar todos los elementos del dominio (modelos, excepciones, schemas).
   
📦 ESTRUCTURA INTERNA:

   core/
   ├── models/                          [MODELOS DE DOMINIO]
   │   ├── producto/
   │   │   ├── propiedades/             [3 properties → 3 mixins]
   │   │   │   ├── stock_bajo.py
   │   │   │   ├── agotado.py
   │   │   │   ├── valor_total.py
   │   │   │   └── propiedades.py       (orchestrator)
   │   │   ├── operaciones/             [3 methods → 3 mixins]
   │   │   │   ├── agregar_stock.py
   │   │   │   ├── reducir_stock.py
   │   │   │   ├── establecer_stock.py
   │   │   │   └── operaciones.py       (orchestrator)
   │   │   ├── serializacion/           [4 methods → 4 mixins]
   │   │   │   ├── to_dict.py
   │   │   │   ├── to_tuple.py
   │   │   │   ├── from_dict.py
   │   │   │   ├── from_row.py
   │   │   │   └── serializacion.py     (orchestrator)
   │   │   └── __init__.py              (Producto class)
   │   │
   │   ├── inventario/
   │   │   ├── gestor_productos/        [5 methods → 5 mixins]
   │   │   │   ├── agregar_producto.py
   │   │   │   ├── obtener_producto.py
   │   │   │   ├── listar_productos.py
   │   │   │   ├── eliminar_producto.py
   │   │   │   ├── existe_producto.py
   │   │   │   └── gestor_productos.py  (orchestrator)
   │   │   ├── gestor_historial/        [2 methods → 2 mixins]
   │   │   │   ├── registrar_movimiento.py
   │   │   │   ├── obtener_historial.py
   │   │   │   └── gestor_historial.py  (orchestrator)
   │   │   └── __init__.py              (Inventario class)
   │   └── __init__.py                  (import Producto, Inventario)
   │
   ├── exceptions/                      [EXCEPCIONES DE DOMINIO]
   │   ├── inventario_error.py          (base exception)
   │   ├── producto_no_encontrado.py
   │   ├── stock_insuficiente.py
   │   ├── datos_invalidos.py
   │   ├── operacion_no_permitida.py
   │   └── __init__.py                  (agregate & export)
   │
   ├── schemas.py                       [VALIDACIÓN DE DATOS]
   ├── __init__.py                      [ESTE ARCHIVO - punto de entrada]

✅ EXPORTA:
   • Producto, Inventario
   • InventarioError, ProductoNoEncontrado, StockInsuficiente, DatosInvalidos, OperacionNoPermitida
   • CrearProductoSchema, ActualizarProductoSchema

💡 USO:
   from core import Producto, Inventario, ProductoNoEncontrado
"""

from .models import Producto, Inventario
from .exceptions import (
    InventarioError,
    ProductoNoEncontrado,
    StockInsuficiente,
    DatosInvalidos,
    OperacionNoPermitida,
)
from .schemas import CrearProductoSchema, ActualizarProductoSchema, MovimientoSchema

__all__ = [
    'Producto',
    'Inventario',
    'InventarioError',
    'ProductoNoEncontrado',
    'StockInsuficiente',
    'DatosInvalidos',
    'OperacionNoPermitida',
    'CrearProductoSchema',
    'ActualizarProductoSchema',
    'MovimientoSchema',
]
