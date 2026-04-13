"""
╔════════════════════════════════════════════════════════════════════════════╗
║              ARCHIVO: core/models/inventario/obtener_historial.py         ║
║              RESPONSABILIDAD: Recuperar historial de movimientos          ║
╚════════════════════════════════════════════════════════════════════════════╝

🎯 ÚNICA RESPONSABILIDAD:
   Recuperar movimientos del historial con filtros y límites.
   
💡 OPERACIÓN:
   • obtener_historial: Recuperar movimientos (filtrados por producto y limitados)
"""

from typing import Optional


class ObtenerHistorialMixin:
    """
    Mixin que agrega consulta de historial a Inventario.
    
    RESPONSABILIDAD: 1
    • Recuperar movimientos del historial con opciones de filtrado
    
    Requiere atributo:
        • self._historial (list)
    """
    
    def obtener_historial(
        self,
        producto_id: Optional[str] = None,
        limite: int = 100,
    ) -> list:
        """
        Obtener historial de movimientos con opciones de filtrado.
        
        Args:
            producto_id: Filtrar por producto específico (opcional)
            limite: Máximo de registros a retornar (default 100, 0 = sin límite)
            
        Returns:
            Lista de movimientos que cumplen los criterios
        """
        historial = self._historial
        
        if producto_id:
            historial = [m for m in historial if m['producto_id'] == producto_id]
        
        return historial[-limite:] if limite else historial
