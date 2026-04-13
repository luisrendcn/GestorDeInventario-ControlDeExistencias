"""
╔════════════════════════════════════════════════════════════════════════════╗
║          ARCHIVO: core/schemas/crear_producto_dataclass.py                ║
║          RESPONSABILIDAD: Estructura de datos para crear producto         ║
╚════════════════════════════════════════════════════════════════════════════╝

🎯 ÚNICA RESPONSABILIDAD:
   Definir la estructura de datos (campos) para crear un producto.
   
💡 CAMPOS:
   • id, nombre, precio, stock, stock_minimo, descripcion
"""

from dataclasses import dataclass


@dataclass
class CrearProductoDataclassMixin:
    """
    Mixin que define estructura de datos para crear producto.
    
    RESPONSABILIDAD: 1
    • Definir campos necesarios para crear un producto
    """
    
    id: str
    nombre: str
    precio: float
    stock: int
    stock_minimo: int = 5
    descripcion: str = ""
