"""
╔════════════════════════════════════════════════════════════════╗
║  ARCHIVO: database/demo_manager.py                            ║
║  FUNCIÓN: Gestión de datos de demostración                    ║
╚════════════════════════════════════════════════════════════════╝

Responsabilidad única: Crear y limpiar datos de demostración
"""

import sqlite3
from typing import List, Dict, Any
from datetime import datetime


class DemoManager:
    """
    Gestiona inicialización y limpieza de datos de demostración.
    
    Responsabilidades:
      • Crear datos demo de ejemplo
      • Limpiar la base de datos
    """
    
    def __init__(self, conn: sqlite3.Connection):
        """Recibir conexión existente."""
        self.conn = conn
    
    def inicializar_datos_demo(self) -> Dict[str, Any]:
        """
        Carga datos de demostración en la base de datos.
        
        Returns:
          Diccionario con estadísticas de inserción
        """
        cursor = self.conn.cursor()
        
        # Limpiar datos existentes primero
        cursor.execute("DELETE FROM movimientos")
        cursor.execute("DELETE FROM productos")
        
        # Productos demo
        productos_demo = [
            ("Laptop Dell", 25000, 10, 3),
            ("Monitor LG 24\"", 8000, 15, 5),
            ("Teclado Mecánico", 3500, 20, 8),
            ("Mouse Logitech", 2000, 30, 10),
            ("Auriculares Sony", 15000, 8, 2),
            ("SSD Samsung 500GB", 12000, 12, 4),
            ("RAM DDR4 8GB", 4500, 20, 6),
            ("Fuente 750W", 6000, 10, 3),
            ("Cable HDMI", 800, 50, 15),
            ("Adaptador USB-C", 1500, 25, 8),
        ]
        
        for nombre, precio, stock, stock_minimo in productos_demo:
            cursor.execute(
                """INSERT INTO productos (nombre, precio, stock, stock_minimo) 
                   VALUES (?, ?, ?, ?)""",
                (nombre, precio, stock, stock_minimo)
            )
        
        # Movimientos demo (registros históricos)
        movimientos_demo = [
            (1, "entrada", 10, "Compra inicial"),
            (2, "entrada", 15, "Compra inicial"),
            (3, "entrada", 20, "Compra inicial"),
            (4, "salida", 5, "Venta"),
            (5, "entrada", 8, "Compra"),
            (1, "salida", 2, "Venta"),
            (2, "salida", 3, "Venta"),
        ]
        
        ahora = datetime.now().isoformat()
        for producto_id, tipo, cantidad, descripcion in movimientos_demo:
            cursor.execute(
                """INSERT INTO movimientos (producto_id, tipo, cantidad, descripcion, fecha)
                   VALUES (?, ?, ?, ?, ?)""",
                (producto_id, tipo, cantidad, descripcion, ahora)
            )
        
        self.conn.commit()
        
        return {
            "productos_insertados": len(productos_demo),
            "movimientos_insertados": len(movimientos_demo),
            "estado": "success"
        }
    
    def limpiar_base_datos(self) -> Dict[str, Any]:
        """
        Limpia todos los datos de la base de datos.
        
        Returns:
          Diccionario con estadísticas de eliminación
        """
        cursor = self.conn.cursor()
        
        # Eliminar todos los registros
        cursor.execute("DELETE FROM movimientos")
        cursor.execute("DELETE FROM productos")
        
        self.conn.commit()
        
        return {
            "estado": "success",
            "mensaje": "Base de datos limpiada correctamente"
        }
