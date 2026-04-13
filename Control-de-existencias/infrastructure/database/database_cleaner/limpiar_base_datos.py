"""
╔════════════════════════════════════════════════════════════════════════════╗
║      ARCHIVO: infrastructure/database/database_cleaner/limpiar_base_datos.py
║      RESPONSABILIDAD: Limpiar la Base de Datos                            ║
╚════════════════════════════════════════════════════════════════════════════╝

🎯 ÚNICA RESPONSABILIDAD:
   Limpiar/resetear toda la BD (para desarrollo y testing).
"""

import sqlite3


class LimpiarBaseDatosMixin:
    """
    Mixin que agrega método para limpiar la BD.
    
    RESPONSABILIDAD: 1
    • Limpiar toda la BD (IRREVERSIBLE)
    
    Requiere atributo:
        • self.conn (conexión SQLite)
    
    ⚠️  ADVERTENCIA CRÍTICA:
      • Esta operación es IRREVERSIBLE
      • Borra TODOS los datos
      • Usar SOLO en desarrollo/testing
      • NUNCA en producción
    """
    
    def limpiar_base_datos(self) -> bool:
        """
        🧹 Limpiar TODA la BD.
        
        Orden:
            1. DELETE FROM movimientos (evitar FK issues)
            2. DELETE FROM productos
        
        Returns:
            bool: True si éxito, False si error
        
        Nota: Idempotente - llamar 2 veces no causa problemas
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM movimientos")
            cursor.execute("DELETE FROM productos")
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"[DB ERROR] {e}")
            return False
