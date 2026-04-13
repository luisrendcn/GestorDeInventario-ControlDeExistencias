"""
╔════════════════════════════════════════════════════════════════════════════╗
║            ARCHIVO: core/schemas/movimiento_dataclass.py                  ║
║            RESPONSABILIDAD: Estructura de datos para movimiento           ║
╚════════════════════════════════════════════════════════════════════════════╝

🎯 ÚNICA RESPONSABILIDAD:
   Definir la estructura de datos (campos) para movimiento de stock.
   
💡 CAMPOS:
   • producto_id, cantidad, motivo (opcional)
"""

from dataclasses import dataclass


@dataclass
class MovimientoDataclassMixin:
    """
    Mixin que define estructura de datos para movimiento.
    
    RESPONSABILIDAD: 1
    • Definir campos necesarios para registrar movimiento de stock
    """
    
    producto_id: str
    cantidad: int
    motivo: str = ""
