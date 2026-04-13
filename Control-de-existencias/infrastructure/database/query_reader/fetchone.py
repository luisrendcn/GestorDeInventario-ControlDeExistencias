"""
╔════════════════════════════════════════════════════════════════════════════╗
║          ARCHIVO: infrastructure/database/query_reader/fetchone.py         ║
║          RESPONSABILIDAD: Obtener un registro                             ║
╚════════════════════════════════════════════════════════════════════════════╝

🎯 ÚNICA RESPONSABILIDAD:
   Ejecutar SELECT que retorna un solo registro.
"""

import sqlite3
from typing import Optional, Tuple


class FetchoneMixin:
    """
    Mixin que agrega método para obtener un registro.
    
    RESPONSABILIDAD: 1
    • Ejecutar SELECT que retorna un registro
    
    Requiere atributo:
        • self.conn (conexión SQLite)
    """
    
    def fetchone(self, query: str, params: Tuple = ()) -> Optional[sqlite3.Row]:
        """
        🔍 Obtener UN SOLO registro.
        
        Args:
            query: SQL SELECT statement con ? placeholders
            params: Valores para WHERE, etc.
        
        Returns:
            sqlite3.Row (acceso por nombre) o None si no existe
        
        Raises:
            sqlite3.Error: Si query es inválida
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"[DB ERROR] {e}")
            raise
