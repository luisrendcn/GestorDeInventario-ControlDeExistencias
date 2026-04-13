"""
╔════════════════════════════════════════════════════════════════╗
║  ARCHIVO: database/history_manager.py                         ║
║  FUNCIÓN: Gestión de historial de movimientos                 ║
╚════════════════════════════════════════════════════════════════╝

Responsabilidad única: Operaciones con historial de movimientos
"""

import sqlite3
from typing import List, Optional, Dict


class HistoryManager:
    """
    Gestiona el historial de movimientos.
    
    Responsabilidades:
      • Obtener historial general
      • Obtener historial de producto específico
      • Registrar movimientos
    """
    
    def __init__(self, conn: sqlite3.Connection):
        """Recibir conexión existente."""
        self.conn = conn
    
    def obtener_historial(self, producto_id: Optional[str] = None, 
                         limite: int = 100) -> List[Dict]:
        """
        Obtiene historial de movimientos.
        
        Args:
          producto_id: Si se especifica, filtrar por producto
          limite: Límite de registros
        
        Returns:
          Lista de movimientos
        """
        cursor = self.conn.cursor()
        
        if producto_id:
            cursor.execute("""
                SELECT * FROM movimientos 
                WHERE producto_id = ? 
                ORDER BY fecha DESC 
                LIMIT ?
            """, (producto_id, limite))
        else:
            cursor.execute("""
                SELECT * FROM movimientos 
                ORDER BY fecha DESC 
                LIMIT ?
            """, (limite,))
        
        return [dict(row) for row in cursor.fetchall()]
    
    def registrar_movimiento(self, producto_id: str, tipo: str, 
                            cantidad: int, stock_anterior: int, 
                            stock_nuevo: int, motivo: str = "") -> bool:
        """
        Registra un movimiento en el historial.
        
        Args:
          producto_id: ID del producto
          tipo: Tipo de movimiento
          cantidad: Cantidad movida
          stock_anterior: Stock antes del movimiento
          stock_nuevo: Stock después del movimiento
          motivo: Razón del movimiento
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO movimientos 
                (producto_id, tipo, cantidad, stock_anterior, stock_nuevo, motivo)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (producto_id, tipo, cantidad, stock_anterior, stock_nuevo, motivo))
            
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            self.conn.rollback()
            raise Exception(f"Error registrando movimiento: {e}")
