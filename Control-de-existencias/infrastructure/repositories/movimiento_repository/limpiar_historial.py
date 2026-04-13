"""
╔════════════════════════════════════════════════════════════════════════════╗
║   ARCHIVO: movimiento_repository/limpiar_historial.py                     ║
║   RESPONSABILIDAD: Limpiar historial de movimientos                       ║
╚════════════════════════════════════════════════════════════════════════════╝

🎯 ÚNICA RESPONSABILIDAD:
   Borrar todos los movimientos (operación irreversible).
"""


class LimpiarHistorialMixin:
    """
    Mixin que agrega método para limpiar historial.
    
    RESPONSABILIDAD: 1
    • Eliminar todos los movimientos
    
    Requiere atributos:
        • self.executor (QueryExecutor)
    
    ⚠️  ADVERTENCIA: Esta operación es IRREVERSIBLE
    """
    
    def limpiar_historial(self) -> bool:
        """
        🧹 Limpiar TODO el historial de movimientos (IRREVERSIBLE).
        
        Ejecuta DELETE FROM movimientos sin condiciones.
        
        RESPONSABILIDAD: Limpiar historial
        
        Returns:
            bool: True si DELETE fue exitoso
        
        ⚠️  ADVERTENCIA: Esta operación es IRREVERSIBLE. 
            Usar solo en desarrollo/testing, nunca en producción.
        
        Usado por: admin_bp.limpiar() para limpiar DB de demo
        """
        return self.executor.ejecutar("DELETE FROM movimientos") > 0
