"""
╔════════════════════════════════════════════════════════════════════════════╗
║        ARCHIVO: core/schemas/actualizar_producto_dataclass.py             ║
║        RESPONSABILIDAD: Estructura de datos para actualizar producto      ║
╚════════════════════════════════════════════════════════════════════════════╝

🎯 ÚNICA RESPONSABILIDAD:
   Definir la estructura de datos (campos opcionales) para actualizar producto.
   
💡 CAMPOS (todos opcionales):
   • nombre, precio, stock_minimo, descripcion
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class ActualizarProductoDataclassMixin:
    """
    Mixin que define estructura para actualizar producto.
    
    RESPONSABILIDAD: 1
    • Definir campos opcionales para actualizar producto
    """
    
    nombre: Optional[str] = None
    precio: Optional[float] = None
    stock_minimo: Optional[int] = None
    descripcion: Optional[str] = None
