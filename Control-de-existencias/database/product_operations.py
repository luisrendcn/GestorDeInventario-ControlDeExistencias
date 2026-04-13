"""
╔════════════════════════════════════════════════════════════════╗
║  ARCHIVO: database/product_operations.py                      ║
║  FUNCIÓN: Operaciones CRUD para productos                     ║
╚════════════════════════════════════════════════════════════════╝

Responsabilidad única: CRUD de productos
"""

import sqlite3
from typing import List, Optional, Dict, Any

from core.models import Producto


class ProductOperations:
    """
    Operaciones CRUD para productos.
    
    Responsabilidades:
      • Crear producto
      • Obtener producto
      • Listar productos
      • Actualizar stock
      • Eliminar producto
    """
    
    def __init__(self, conn: sqlite3.Connection):
        """Recibir conexión existente."""
        self.conn = conn
    
    def crear_producto(self, producto: Producto) -> bool:
        """Crea un producto en BD."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO productos 
                (id, nombre, precio, stock, stock_minimo, descripcion)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (producto.id, producto.nombre, producto.precio, 
                  producto.stock, producto.stock_minimo, producto.descripcion))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            self.conn.rollback()
            raise ValueError(f"Producto {producto.id} ya existe")
        except sqlite3.Error as e:
            self.conn.rollback()
            raise Exception(f"Error creando producto: {e}")
    
    def obtener_producto(self, producto_id: str) -> Optional[Dict]:
        """Obtiene un producto por ID."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM productos WHERE id = ?", (producto_id,))
        row = cursor.fetchone()
        
        if row:
            return dict(row)
        return None
    
    def listar_productos(self) -> List[Dict]:
        """Lista todos los productos."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM productos ORDER BY nombre")
        return [dict(row) for row in cursor.fetchall()]
    
    def actualizar_stock(self, producto_id: str, nuevo_stock: int, 
                        tipo: str, cantidad: int, motivo: str = "") -> bool:
        """
        Actualiza stock y registra movimiento.
        
        Args:
          producto_id: ID del producto
          nuevo_stock: Nuevo valor de stock
          tipo: Tipo de movimiento (ENTRADA, SALIDA, AJUSTE)
          cantidad: Cantidad movida
          motivo: Razón del movimiento
        """
        try:
            cursor = self.conn.cursor()
            
            # Obtener stock anterior
            cursor.execute("SELECT stock FROM productos WHERE id = ?", (producto_id,))
            resultado = cursor.fetchone()
            if not resultado:
                raise ValueError(f"Producto {producto_id} no existe")
            
            stock_anterior = resultado[0]
            
            # Actualizar stock
            cursor.execute(
                "UPDATE productos SET stock = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (nuevo_stock, producto_id)
            )
            
            # Registrar movimiento
            cursor.execute("""
                INSERT INTO movimientos 
                (producto_id, tipo, cantidad, motivo, stock_anterior, stock_nuevo)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (producto_id, tipo, cantidad, motivo, stock_anterior, nuevo_stock))
            
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            self.conn.rollback()
            raise Exception(f"Error actualizando stock: {e}")
    
    def eliminar_producto(self, producto_id: str) -> bool:
        """Elimina un producto."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM productos WHERE id = ?", (producto_id,))
            self.conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            self.conn.rollback()
            raise Exception(f"Error eliminando producto: {e}")
