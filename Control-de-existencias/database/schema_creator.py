"""
╔════════════════════════════════════════════════════════════════╗
║  ARCHIVO: database/schema_creator.py                          ║
║  FUNCIÓN: Crear esquema de tablas                             ║
╚════════════════════════════════════════════════════════════════╝

Responsabilidad única: DDL (CREATE TABLE) de BD
"""

import sqlite3


class SchemaCreator:
    """
    Crea esquema (tablas) en SQLite.
    
    Responsabilidades:
      • Crear tabla productos
      • Crear tabla movimientos
      • Manejar migraciones
    """
    
    def __init__(self, conn: sqlite3.Connection):
        """Recibir conexión existente."""
        self.conn = conn
    
    def crear_tablas(self):
        """Crea todas las tablas si no existen."""
        self._crear_tabla_productos()
        self._crear_tabla_movimientos()
        print("[DB] Tablas creadas/verificadas")
    
    def _crear_tabla_productos(self):
        """Crea tabla de productos."""
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                id TEXT PRIMARY KEY,
                nombre TEXT NOT NULL,
                precio REAL NOT NULL,
                stock INTEGER NOT NULL DEFAULT 0,
                stock_minimo INTEGER NOT NULL DEFAULT 5,
                descripcion TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()
    
    def _crear_tabla_movimientos(self):
        """Crea tabla de movimientos (auditoría)."""
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS movimientos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                producto_id TEXT NOT NULL,
                tipo TEXT NOT NULL,
                cantidad INTEGER NOT NULL,
                stock_anterior INTEGER,
                stock_nuevo INTEGER,
                motivo TEXT,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE CASCADE
            )
        """)
        self.conn.commit()
