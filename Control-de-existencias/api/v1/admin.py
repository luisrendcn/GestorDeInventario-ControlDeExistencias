"""
ARCHIVO: api/v1/admin.py
FUNCIÓN: Blueprint de administración - endpoints de inicialización y limpieza
"""

from flask import Blueprint, jsonify
import sqlite3
from pathlib import Path


def crear_admin_bp() -> Blueprint:
    """Crear blueprint de administración."""
    bp = Blueprint('admin', __name__)
    
    @bp.route('/inicializar', methods=['POST'])
    def inicializar():
        """Inicializar BD con datos de demo."""
        try:
            print("[ADMIN] Iniciando...")
            # Obtener ruta de BD desde ubicación relativa
            db_path = Path(__file__).parent.parent.parent / "control_existencias.db"
            print(f"[ADMIN] BD en: {db_path}")
            
            # Crear nueva conexión para esta operación
            print("[ADMIN] Abriendo conexión...")
            conn = sqlite3.connect(str(db_path), check_same_thread=False, timeout=5.0)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            print("[ADMIN] Conexión abierta")
            
            # Productos de demo
            productos_demo = [
                ('P001', 'Laptop Dell', 899.99, 10, 5, 'Laptop de trabajo'),
                ('P002', 'Mouse Logitech', 29.99, 50, 10, 'Mouse inalámbrico'),
                ('P003', 'Teclado Mecánico', 149.99, 15, 5, 'Teclado RGB'),
                ('P004', 'Monitor 27"', 349.99, 8, 3, 'Monitor 4K'),
                ('P005', 'Webcam HD', 79.99, 0, 5, 'Webcam 1080p'),
            ]
            
            insertados = 0
            for p in productos_demo:
                try:
                    cursor.execute(
                        "INSERT OR IGNORE INTO productos (id, nombre, precio, stock, stock_minimo, descripcion) VALUES (?, ?, ?, ?, ?, ?)",
                        p
                    )
                    insertados += cursor.rowcount
                except Exception as e:
                    print(f"[ADMIN] Error insertando {p[0]}: {e}")
            
            print(f"[ADMIN] Commiteando {insertados} inserts...")
            conn.commit()
            print(f"[ADMIN] Commit exitoso")
            
            # Contar total
            cursor.execute("SELECT COUNT(*) as total FROM productos")
            total_row = cursor.fetchone()
            total = total_row["total"] if total_row else 0
            print(f"[ADMIN] Total en BD: {total}")
            
            # Cerrar conexión
            conn.close()
            print("[ADMIN] Conexión cerrada")
            
            return jsonify({
                "mensaje": "✅ Base de datos inicializada con datos de demo",
                "productos_creados": insertados,
                "total_en_bd": total,
            }), 200
        except Exception as e:
            print(f"[ADMIN ERROR] {type(e).__name__}: {str(e)}")
            import traceback
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500
    
    @bp.route('/limpiar', methods=['POST'])
    def limpiar():
        """Limpiar BD (IRREVERSIBLE)."""
        try:
            db_path = Path(__file__).parent.parent.parent / "control_existencias.db"
            conn = sqlite3.connect(str(db_path), check_same_thread=False)
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM movimientos")
            cursor.execute("DELETE FROM productos")
            
            conn.commit()
            conn.close()
            
            return jsonify({
                "mensaje": "✅ Base de datos limpiada correctamente",
                "advertencia": "Todos los datos han sido eliminados"
            }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    return bp
