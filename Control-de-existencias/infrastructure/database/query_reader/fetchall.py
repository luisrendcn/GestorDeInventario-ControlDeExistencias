"""
╔════════════════════════════════════════════════════════════════════════════╗
║          ARCHIVO: infrastructure/database/query_reader/fetchall.py         ║
║          RESPONSABILIDAD: Obtener múltiples registros                     ║
╚════════════════════════════════════════════════════════════════════════════╝

🎯 ÚNICA RESPONSABILIDAD:
   Ejecutar SELECT que retorna múltiples registros.
"""

import sqlite3
from typing import List, Tuple


class FetchallMixin:
    """
    Mixin que agrega método para obtener múltiples registros.
    
    RESPONSABILIDAD: 1
    • Ejecutar SELECT que retorna múltiples registros
    
    Requiere atributo:
        • self.conn (conexión SQLite)
    """
    
    def fetchall(self, query: str, params: Tuple = ()) -> List[sqlite3.Row]:
        """
        📋 Obtener TODOS los registros.
        
        Args:
            query: SQL SELECT statement con ? placeholders
            params: Valores para WHERE, LIMIT, ORDER BY, etc.
        
        Returns:
            List[sqlite3.Row] (puede estar vacía [])
        
        Raises:
            sqlite3.Error: Si query es inválida
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"[DB ERROR] {e}")
            raise
