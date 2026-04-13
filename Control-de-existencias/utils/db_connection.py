"""
Gestor robusto de conexión a BD con reconexión automática.
"""

import sqlite3
from pathlib import Path
from typing import Optional


class DatabaseConnection:
    """Manejador de conexión con reconexión automática."""
    
    _instance = None
    _db_path: Optional[str] = None
    _conn: Optional[sqlite3.Connection] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @classmethod
    def init(cls, db_path: str):
        """Inicializar con la ruta de BD."""
        cls._db_path = db_path
        instance = cls()
        instance._ensure_connection()
        return instance
    
    def _ensure_connection(self):
        """Asegurar que hay una conexión abierta."""
        if self._conn is None:
            self._connect()
        else:
            # Verificar si está viva
            try:
                self._conn.execute("SELECT 1")
            except sqlite3.Error:
                self._connection = None
                self._connect()
    
    def _connect(self):
        """Conectar a la BD."""
        try:
            if self._db_path is None:
                raise RuntimeError("Database path not initialized")
            
            # Cerrar cualquier conexión vieja
            if self._conn:
                try:
                    self._conn.close()
                except:
                    pass
            
            self._conn = sqlite3.connect(self._db_path, check_same_thread=False)
            self._conn.row_factory = sqlite3.Row
            print(f"[DB] ✓ Conectado: {Path(self._db_path).name}")
        except sqlite3.Error as e:
            print(f"[DB] ✗ Error de conexión: {e}")
            self._conn = None
            raise
    
    def get(self) -> sqlite3.Connection:
        """Obtener conexión garantizada."""
        self._ensure_connection()
        if self._conn is None:
            raise RuntimeError("Cannot establish database connection")
        return self._conn
    
    def execute(self, query: str, params: tuple = ()):
        """Ejecutar query con reconexión automática."""
        try:
            conn = self.get()
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor
        except sqlite3.Error as e:
            print(f"[DB] Error ejecutando query: {e}")
            raise
    
    def fetchone(self, query: str, params: tuple = ()):
        """Obtener un registro."""
        try:
            conn = self.get()
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"[DB] Error obteniendo registro: {e}")
            raise
    
    def fetchall(self, query: str, params: tuple = ()):
        """Obtener todos los registros."""
        try:
            conn = self.get()
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"[DB] Error obteniendo registros: {e}")
            raise
    
    def close(self):
        """Cerrar conexión."""
        if self._conn:
            try:
                self._conn.close()
            except:
                pass
            self._conn = None
