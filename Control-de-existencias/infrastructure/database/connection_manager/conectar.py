"""
╔════════════════════════════════════════════════════════════════════════════╗
║         ARCHIVO: infrastructure/database/connection_manager/conectar.py    ║
║         RESPONSABILIDAD: Conectar a la Base de Datos                      ║
╚════════════════════════════════════════════════════════════════════════════╝

🎯 ÚNICA RESPONSABILIDAD:
   Establecer conexión a SQLite configurando parámetros.
"""

import sqlite3


class ConectarMixin:
    """
    Mixin que agrega método para conectar a la BD.
    
    RESPONSABILIDAD: 1
    • Establecer conexión SQLite con configuración
    
    Requiere atributos:
        • self.db_path (str)
        • self.conn (será asignado)
    """
    
    def conectar(self):
        """
        🔌 Establecer conexión a BD.
        
        Configura:
          • sqlite3.connect() con check_same_thread=False
          • row_factory = sqlite3.Row para acceso por nombre
          • Print de confirmación
        """
        try:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
            print(f"[DB] Conectado a SQLite: {self.db_path}")
        except sqlite3.Error as e:
            print(f"[DB ERROR] No se pudo conectar: {e}")
            raise
