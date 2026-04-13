"""
╔════════════════════════════════════════════════════════════════╗
║  ARCHIVO: database/report_generator.py                        ║
║  FUNCIÓN: Generación de reportes                              ║
╚════════════════════════════════════════════════════════════════╝

Responsabilidad única: Generar reportes de inventario
"""

import sqlite3
from typing import Dict, Any


class ReportGenerator:
    """
    Genera reportes de inventario.
    
    Responsabilidades:
      • Calcular estadísticas generales
      • Generar reporte de existencias
      • Alertas de bajo stock
    """
    
    def __init__(self, conn: sqlite3.Connection):
        """Recibir conexión existente."""
        self.conn = conn
    
    def obtener_reporte(self) -> Dict[str, Any]:
        """
        Genera reporte completo de existencias.
        
        Returns:
          Diccionario con estadísticas generales y por estado
        """
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
    
    def obtener_alertas(self) -> Dict[str, Any]:
        """
        Obtiene alertas de inventario.
        
        Returns:
          Diccionario con productos en alerta
        """
        cursor = self.conn.cursor()
        
        # Bajo stock
        cursor.execute("""
            SELECT id, nombre, stock, stock_minimo 
            FROM productos 
            WHERE stock <= stock_minimo AND stock > 0
            ORDER BY stock ASC
        """)
        bajo_stock = [dict(row) for row in cursor.fetchall()]
        
        # Agotados
        cursor.execute("""
            SELECT id, nombre 
            FROM productos 
            WHERE stock = 0
            ORDER BY nombre
        """)
        agotados = [dict(row) for row in cursor.fetchall()]
        
        return {
            "bajo_stock": bajo_stock,
            "agotados": agotados,
            "total_alertas": len(bajo_stock) + len(agotados)
        }
