"""
╔════════════════════════════════════════════════════════════════╗
║  ARCHIVO: database/connection.py                              ║
║  FUNCIÓN: Gestión de conexión a SQLite                       ║
╚════════════════════════════════════════════════════════════════╝

Responsabilidad única: Conectar/desconectar de SQLite
"""

import sqlite3
import os


class DatabaseConnection:
    """
    Gestor de conexión a SQLite.
    
    Responsabilidades:
      • Crear conexión SQLite
      • Configurar row_factory
      • Cerrar conexión
    """
    
    def __init__(self, db_path: str = None):
        """Inicializar con ruta de BD."""
        self.db_path = db_path or os.getenv("DB_PATH", "control_existencias.db")
        self.conn = None
    
    def conectar(self):
        """Establece conexión a BD."""
        try:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
            print(f"[DB] Conectado a SQLite: {self.db_path}")
            return self.conn
        except sqlite3.Error as e:
            print(f"[DB ERROR] No se pudo conectar: {e}")
            raise
    
    def desconectar(self):
        """Cierra conexión a BD."""
        try:
            if self.conn:
                self.conn.close()
                self.conn = None
                print("[DB] Desconectado")
        except Exception as e:
            print(f"[DB] Error al desconectar: {e}")
    
    def cerrar(self):
        """Alias para desconectar()."""
        self.desconectar()
