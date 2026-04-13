"""
╔════════════════════════════════════════════════════════════════════════════╗
║   ARCHIVO: movimiento_repository/obtener_historial.py                     ║
║   RESPONSABILIDAD: Leer historial de movimientos                          ║
╚════════════════════════════════════════════════════════════════════════════╝

🎯 ÚNICA RESPONSABILIDAD:
   Recuperar movimientos con filtros y paginación.
"""

from typing import List, Optional


class ObtenerHistorialMixin:
    """
    Mixin que agrega método para obtener historial.
    
    RESPONSABILIDAD: 1
    • Recuperar movimientos filtrados
    
    Requiere atributos:
        • self.reader (QueryReader)
    """
    
    def obtener_historial(
        self,
        producto_id: Optional[str] = None,
        limite: int = 100,
    ) -> List[dict]:
        """
        📊 Obtener historial de movimientos (filtrable y paginado).
        
        Ejecuta SELECT FROM movimientos con filtros opcionales.
        
        RESPONSABILIDAD: Leer historial
        
        Args:
            producto_id: Si se proporciona, filtra solo movimientos
                         de este producto. Si es None, retorna
                         movimientos de todos los productos.
            limite: Máximo número de registros (default 100, max 100)
        
        Returns:
            List[dict]: Lista de diccionarios con datos de movimientos,
                        ordenados por fecha DESC (más recientes primero)
        
        Flujo:
            1. Si producto_id: SELECT filtrado por producto_id
            2. Si no producto_id: SELECT de TODOS los movimientos
            3. ORDER BY fecha DESC para más recientes primero
            4. LIMIT para paginar
            5. Convertir cada row a dict
        
        Usado por: ReporteService.obtener_historial()
        """
        if producto_id:
            query = """
                SELECT * FROM movimientos 
                WHERE producto_id = ? 
                ORDER BY fecha DESC 
                LIMIT ?
            """
            rows = self.reader.fetchall(query, (producto_id, limite))
        else:
            query = "SELECT * FROM movimientos ORDER BY fecha DESC LIMIT ?"
            rows = self.reader.fetchall(query, (limite,))
        
        return [dict(row) for row in rows]
