"""
╔════════════════════════════════════════════════════════════════════════════╗
║       ARCHIVO: infrastructure/database/query_executor/ejecutar.py          ║
║       RESPONSABILIDAD: Ejecutar queries de modificación                   ║
╚════════════════════════════════════════════════════════════════════════════╝

🎯 ÚNICA RESPONSABILIDAD:
   Ejecutar queries de INSERT/UPDATE/DELETE.
"""

import sqlite3
from typing import Tuple


class EjecutarMixin:
    """
    Mixin que agrega método para ejecutar queries de modificación.
    
    RESPONSABILIDAD: 1
    • Ejecutar queries que CAMBIAN datos (INSERT/UPDATE/DELETE)
    
    Requiere atributo:
        • self.conn (conexión SQLite)
    """
    
    def ejecutar(self, query: str, params: Tuple = ()) -> int:
        """
        ✏️  Ejecutar query de modificación.
        
        Args:
            query: SQL con placeholders (?) para INSERT/UPDATE/DELETE
            params: Valores para reemplazar ?
        
        Returns:
            int: rowcount (filas afectadas)
        
        Raises:
            sqlite3.Error: Si query es inválida
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            self.conn.commit()
            return cursor.rowcount
        except sqlite3.Error as e:
            print(f"[DB ERROR] {e}")
            raise
