"""
historial/obtener_historial.py
===============================
Operación: Obtener historial de movimientos.

Responsabilidad única:
    - Recuperar y filtrar registros de movimientos
"""

from typing import List, Dict, Optional


class ObtenerHistorialMixin:
    """Mixin especializado en consultar historial de movimientos."""

    def obtener_historial(self, producto_id: Optional[str] = None) -> List[Dict]:
        """
        Obtiene el historial de movimientos del inventario.
        
        Permite filtrar por producto específico o retornar todo el historial.
        
        Args:
            producto_id: ID del producto para filtrar (opcional)
            
        Returns:
            Lista de movimientos (cada uno es un dict con timestamp, producto_id, tipo, cantidad)
        """
        if producto_id:
            return [
                m for m in self._historial_movimientos 
                if m['producto_id'] == producto_id
            ]
        return list(self._historial_movimientos)
