"""
╔════════════════════════════════════════════════════════════════════════════╗
║                  ARCHIVO: db.py                                           ║
║                  FUNCIÓN: Capa de persistencia (Gestión de BD)            ║
╚════════════════════════════════════════════════════════════════════════════╝

📋 RESPONSABILIDAD DEL ARCHIVO:
   Gestiona la conexión y todas las operaciones de base de datos SQLite
   de forma centralizada.

🎯 FUNCIONALIDADES:
   ✓ Conexión a BD SQLite
   ✓ Creación automática de tablas (migrations)
   ✓ Operaciones CRUD genéricas
   ✓ Gestión de ciclo de vida (conectar/desconectar)

═════════════════════════════════════════════════════════════════════════════

📦 CLASES:

┌─ class Database (RESPONSABILIDADES: 5)
│
├─ Responsabilidad 1: Gestionar conexión a SQLite
│  └─ __init__() - inicializa ruta de BD
│  └─ conectar() - crea conexión y tablas
│  └─ desconectar() / cerrar() - cierra conexión
│
├─ Responsabilidad 2: Crear esquema de tablas
│  └─ _crear_tablas() - DDL de tablas
│
├─ Responsabilidad 3: Operaciones CRUD
│  └─ ejecutar() - INSERT, UPDATE, DELETE
│  └─ fetchone() - SELECT un registro
│  └─ fetchall() - SELECT múltiples registros
│
├─ Responsabilidad 4: Operaciones de transacciones
│  └─ commit() - guardar cambios
│  └─ rollback() - revertir cambios
│
└─ Responsabilidad 5: Operaciones de limpieza
   └─ limpiar_base_datos() - borrar todo (para demos)

⚠️ NOTA: Está un poco acoplada. Idealmente:
   • Las queries deberían estar en repositories
   • Solo mantener conexión y operaciones genéricas
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Optional, Dict, Any

from core.models import Producto


class Database:
    """
    Gestor de conexión y operaciones en SQLite.
    
    RESPONSABILIDADES: 5
    1. Gestionar conexión a BD
    2. Crear esquema de tablas
    3. Realizar operaciones CRUD
    4. Manejar transacciones
    5. Operaciones de limpieza/demo
    """
    
    def __init__(self):
        """Inicializa conexión a BD SQLite."""
        self.db_path = os.getenv("DB_PATH", "control_existencias.db")
        self.conn = None
    
    def conectar(self):
        """Establece conexión a BD."""
        try:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
            print(f"[DB] Conectado a SQLite: {self.db_path}")
            self._crear_tablas()
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
    
    
    def _crear_tablas(self):
        """Crea tablas si no existen."""
        cursor = self.conn.cursor()
        
        # Tabla de productos
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
        
        # Tabla de movimientos (auditoría)
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
        print("[DB] Tablas creadas/verificadas")
    
    # ========================================================================
    # OPERACIONES CRUD - PRODUCTOS
    # ========================================================================
    
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
        """Actualiza stock y registra movimiento."""
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
    
    def obtener_historial(self, producto_id: Optional[str] = None, 
                         limite: int = 100) -> List[Dict]:
        """Obtiene historial de movimientos."""
        cursor = self.conn.cursor()
        
        if producto_id:
            cursor.execute("""
                SELECT * FROM movimientos 
                WHERE producto_id = ? 
                ORDER BY fecha DESC 
                LIMIT ?
            """, (producto_id, limite))
        else:
            cursor.execute("""
                SELECT * FROM movimientos 
                ORDER BY fecha DESC 
                LIMIT ?
            """, (limite,))
        
        return [dict(row) for row in cursor.fetchall()]
    
    def obtener_reporte(self) -> Dict[str, Any]:
        """Genera reporte de existencias."""
        cursor = self.conn.cursor()
        
        # Estadísticas generales
        cursor.execute("""
            SELECT 
                COUNT(*) as total_productos,
                SUM(stock) as total_unidades,
                SUM(precio * stock) as valor_total,
                AVG(stock) as stock_promedio,
                AVG(precio) as precio_promedio
            FROM productos
        """)
        stats = cursor.fetchone()
        
        # Productos por estado
        cursor.execute("""
            SELECT 
                COUNT(CASE WHEN stock > stock_minimo THEN 1 END) as disponibles,
                COUNT(CASE WHEN stock <= stock_minimo AND stock > 0 THEN 1 END) as stock_bajo,
                COUNT(CASE WHEN stock = 0 THEN 1 END) as agotados
            FROM productos
        """)
        estatus = cursor.fetchone()
        
        return {
            "total_productos": stats[0] or 0,
            "total_unidades": stats[1] or 0,
            "valor_total": float(stats[2]) if stats[2] else 0.0,
            "stock_promedio": float(stats[3]) if stats[3] else 0.0,
            "precio_promedio": float(stats[4]) if stats[4] else 0.0,
            "productos_disponibles": estatus[0] or 0,
            "productos_stock_bajo": estatus[1] or 0,
            "productos_agotados": estatus[2] or 0,
        }
    
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
    
    def inicializar_datos_demo(self) -> List[Dict]:
        """
        Simula que el inventario viene de otro módulo.
        Crea datos de prueba para demostración del sistema.
        
        Returns:
            Lista de productos inicializados
        """
        # Limpiar datos existentes
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM movimientos")
        cursor.execute("DELETE FROM productos")
        self.conn.commit()
        
        # Datos de prueba - simulando que vienen de otro módulo
        productos_demo = [
            {
                'id': 'LAPTOP-001',
                'nombre': 'Laptop Dell XPS 15',
                'precio': 1299.99,
                'stock': 5,
                'stock_minimo': 3,
                'descripcion': 'Laptop de alto rendimiento para profesionales'
            },
            {
                'id': 'MOUSE-002',
                'nombre': 'Mouse Logitech MX Master',
                'precio': 99.99,
                'stock': 2,
                'stock_minimo': 5,
                'descripcion': 'Mouse ergonómico con bluetooth'
            },
            {
                'id': 'TECLADO-003',
                'nombre': 'Teclado Mecánico RGB',
                'precio': 149.99,
                'stock': 8,
                'stock_minimo': 4,
                'descripcion': 'Teclado mecánico con switches Cherry MX'
            },
            {
                'id': 'MONITOR-004',
                'nombre': 'Monitor LG 27" 4K',
                'precio': 399.99,
                'stock': 0,
                'stock_minimo': 2,
                'descripcion': 'Monitor 4K IPS de 27 pulgadas'
            },
            {
                'id': 'CABLE-USB-005',
                'nombre': 'Cable USB Tipo C',
                'precio': 9.99,
                'stock': 50,
                'stock_minimo': 20,
                'descripcion': 'Cable USB 3.1 tipo C'
            },
            {
                'id': 'AURICULAR-006',
                'nombre': 'Auricular Sony WH-1000XM5',
                'precio': 399.99,
                'stock': 1,
                'stock_minimo': 3,
                'descripcion': 'Auricular inalámbrico con cancelación de ruido'
            },
            {
                'id': 'WEBCAM-007',
                'nombre': 'Webcam Logitech 4K',
                'precio': 179.99,
                'stock': 3,
                'stock_minimo': 2,
                'descripcion': 'Cámara web 4K con micrófono incorporado'
            },
            {
                'id': 'HDD-008',
                'nombre': 'Disco Duro 2TB Seagate',
                'precio': 79.99,
                'stock': 12,
                'stock_minimo': 5,
                'descripcion': 'Disco duro externo de 2TB'
            },
            {
                'id': 'SSD-009',
                'nombre': 'SSD 1TB Samsung 970 EVO',
                'precio': 149.99,
                'stock': 0,
                'stock_minimo': 3,
                'descripcion': 'SSD NVMe de 1TB'
            },
            {
                'id': 'RAM-010',
                'nombre': 'Memoria RAM 16GB DDR4',
                'precio': 89.99,
                'stock': 7,
                'stock_minimo': 4,
                'descripcion': 'Memoria RAM 16GB DDR4 3200MHz'
            }
        ]
        
        # Insertar productos
        try:
            for prod_data in productos_demo:
                producto = Producto(
                    id=prod_data['id'],
                    nombre=prod_data['nombre'],
                    precio=prod_data['precio'],
                    stock=prod_data['stock'],
                    stock_minimo=prod_data['stock_minimo'],
                    descripcion=prod_data['descripcion']
                )
                self.crear_producto(producto)
                
                # Registrar movimiento inicial
                cursor = self.conn.cursor()
                cursor.execute("""
                    INSERT INTO movimientos 
                    (producto_id, tipo, cantidad, motivo, stock_anterior, stock_nuevo)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (producto.id, 'entrada_inicial', producto.stock, 
                      'Inventario inicial del módulo', 0, producto.stock))
            
            self.conn.commit()
            print(f"[DB] ✅ {len(productos_demo)} productos de demostración creados")
            return self.listar_productos()
        
        except Exception as e:
            self.conn.rollback()
            raise Exception(f"Error inicializando datos: {e}")
    
    def limpiar_base_datos(self) -> bool:
        """
        Limpia todos los datos de la base de datos.
        Útil para reiniciar el sistema.
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM movimientos")
            cursor.execute("DELETE FROM productos")
            self.conn.commit()
            print("[DB] ✅ Base de datos limpiada")
            return True
        except sqlite3.Error as e:
            self.conn.rollback()
            raise Exception(f"Error limpiando base de datos: {e}")


# Instancia global
db = Database()
