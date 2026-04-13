"""
╔════════════════════════════════════════════════════════════════════════════╗
║              ARCHIVO: core/models/inventario/registrar_movimiento.py       ║
║              RESPONSABILIDAD: Registrar movimientos en auditoría           ║
╚════════════════════════════════════════════════════════════════════════════╝

🎯 ÚNICA RESPONSABILIDAD:
   Crear una entrada de auditoría cuando ocurre un movimiento de stock.
   
💡 OPERACIÓN:
   • registrar_movimiento: Registrar un movimiento (entrada/salida/ajuste)
"""

from datetime import datetime


class RegistrarMovimientoMixin:
    """
    Mixin que agrega registro de movimientos a Inventario.
    
    RESPONSABILIDAD: 1
    • Crear entrada de auditoría para movimientos de stock
    
    Requiere atributo:
        • self._historial (list)
    """
    
    def registrar_movimiento(
        self,
        producto_id: str,
        tipo: str,
        cantidad: int,
        motivo: str = "",
    ):
        """
        Registrar movimiento de stock en el historial de auditoría.
        
        Args:
            producto_id: ID del producto afectado
            tipo: Tipo de movimiento (ENTRADA, SALIDA, AJUSTE)
            cantidad: Cantidad movida
            motivo: Razón del movimiento (opcional)
        """
        movimiento = {
            'timestamp': datetime.now().isoformat(),
            'producto_id': producto_id,
            'tipo': tipo,
            'cantidad': cantidad,
            'motivo': motivo,
        }
        self._historial.append(movimiento)
