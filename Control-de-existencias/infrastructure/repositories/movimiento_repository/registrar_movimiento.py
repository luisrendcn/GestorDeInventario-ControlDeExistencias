"""
╔════════════════════════════════════════════════════════════════════════════╗
║   ARCHIVO: movimiento_repository/registrar_movimiento.py                  ║
║   RESPONSABILIDAD: Registrar movimiento en el historial                   ║
╚════════════════════════════════════════════════════════════════════════════╝

🎯 ÚNICA RESPONSABILIDAD:
   Insertar un nuevo movimiento de stock en la auditoría.
"""


class RegistrarMovimientoMixin:
    """
    Mixin que agrega método para registrar movimientos.
    
    RESPONSABILIDAD: 1
    • Persistir movimiento de stock
    
    Requiere atributos:
        • self.executor (QueryExecutor)
    """
    
    def registrar_movimiento(
        self,
        producto_id: str,
        tipo: str,
        cantidad: int,
        stock_anterior: int = None,
        stock_nuevo: int = None,
        motivo: str = "",
    ) -> bool:
        """
        📍 Registrar un movimiento de stock en el historial.
        
        Ejecuta INSERT INTO movimientos para auditoría y trazabilidad.
        
        RESPONSABILIDAD: Persistir movimientos
        
        Args:
            producto_id: ID del producto afectado
            tipo: Tipo de movimiento (ENTRADA, SALIDA, AJUSTE)
            cantidad: Cantidad del movimiento
            stock_anterior: Stock antes del movimiento (opcional)
            stock_nuevo: Stock después del movimiento (opcional)
            motivo: Razón del movimiento (e.g., "Compra", "Venta")
        
        Returns:
            bool: True si INSERT fue exitoso
        
        Flujo:
            1. Construir query INSERT con placeholders
            2. Timestamp se asigna automáticamente en BD (DEFAULT)
            3. Ejecutar mediante QueryExecutor.ejecutar()
        
        Usado por: InventarioService después de cada movimiento
        """
        query = """
            INSERT INTO movimientos 
            (producto_id, tipo, cantidad, stock_anterior, stock_nuevo, motivo)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        params = (producto_id, tipo, cantidad, stock_anterior, stock_nuevo, motivo)
        return self.executor.ejecutar(query, params) > 0
