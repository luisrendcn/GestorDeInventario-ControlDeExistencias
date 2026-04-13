"""
╔════════════════════════════════════════════════════════════════════════════╗
║                  ARCHIVO: core/exceptions/operacion_no_permitida.py       ║
║                  RESPONSABILIDAD: Operación prohibida                      ║
╚════════════════════════════════════════════════════════════════════════════╝

🎯 ÚNICA RESPONSABILIDAD:
   Indicar que una operación está prohibida en el contexto actual.
   
💡 CASOS:
   • Eliminar producto que está en transacciones activas
   • Modificar producto en estado bloqueado
   • Operación requiere permisos especiales no otorgados
"""

from core.exceptions.inventario_error import InventarioError


class OperacionNoPermitida(InventarioError):
    """
    La operación no está permitida.
    
    RESPONSABILIDAD: 1
    • Indicar que la operación está prohibida en contexto actual
    
    Ejemplo:
        • Eliminar producto que está en venta
        • Modificar stock de producto bloqueado
    """
    pass
