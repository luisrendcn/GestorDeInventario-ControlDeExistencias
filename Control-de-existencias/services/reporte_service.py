"""
╔════════════════════════════════════════════════════════════════════════════╗
║                  ARCHIVO: services/reporte_service.py                     ║
║                  FUNCIÓN: Servicios de reportes y análisis                ║
╚════════════════════════════════════════════════════════════════════════════╝

📋 RESPONSABILIDAD DEL ARCHIVO:
   Implementar la lógica de negocio para generar reportes y análisis
   del estado del inventario.

🎯 FUNCIONALIDADES:
   ✓ Reporte general del inventario
   ✓ Alertas de stock
   ✓ Historial de movimientos
   ✓ Productos con mayor/menor stock
   ✓ Valor total del inventario

═════════════════════════════════════════════════════════════════════════════

📦 CLASES:

┌─ class ReporteService (RESPONSABILIDADES: 6)
│  ├─ Responsabilidad 1: Reporte general
│  │  └─ obtener_reporte() - estadísticas globales
│  │
│  ├─ Responsabilidad 2: Alertas
│  │  └─ obtener_alertas() - productos en alerta
│  │
│  ├─ Responsabilidad 3: Historial
│  │  └─ obtener_historial() - movimientos de stock
│  │
│  ├─ Responsabilidad 4: Ordenamiento por stock
│  │  ├─ obtener_productos_mayor_stock()
│  │  └─ obtener_productos_menor_stock()
│  │
│  └─ Responsabilidad 5: Valuación
│     └─ obtener_valor_total_inventario()
│
🔗 HERENCIA:
   ReporteService extends BaseService
   • Hereda: self.repository, validar_producto_existe()

🔄 CASOS DE USO:
   • Dashboard: mostrar resumen del inventario
   • Alertas: notificar productos con stock bajo
   • Auditoría: verificar historial de cambios
   • Análisis: reportes ejecutivos
"""

from typing import Dict, List, Any, Optional
from .base_service import Service


class ReporteService(Service):
    """
    Servicios de reportes y análisis.
    
    RESPONSABILIDADES: 6
    1. Generar reporte general (obtener_reporte)
    2. Generar alertas (obtener_alertas)
    3. Obtener historial (obtener_historial)
    4. Ordenar por mayor stock (obtener_productos_mayor_stock)
    5. Ordenar por menor stock (obtener_productos_menor_stock)
    6. Valuación total (obtener_valor_total_inventario)
    """
    
    def obtener_reporte(self) -> Dict[str, Any]:
        """
        Obtener reporte general del inventario.
        
        RESPONSABILIDADES: 1
        • Calcular estadísticas del inventario
        
        Returns:
            dict: Reporte con:
              • total_productos: Cantidad de productos únicos
              • total_unidades: Suma de todos los stocks
              • valor_total: Valuación total
              • stock_promedio: Promedio de stock por producto
              • precio_promedio: Promedio de precios
              • productos_disponibles: Con stock y no bajo mínimo
              • productos_agotados: Con stock = 0
              • productos_con_stock_bajo: stock <= stock_minimo
        """
        productos = self.repository.listar()
        
        if not productos:
            return {
                'total_productos': 0,
                'total_unidades': 0,
                'valor_total': 0.0,
                'stock_promedio': 0.0,
                'precio_promedio': 0.0,
                'productos_disponibles': 0,
                'productos_agotados': 0,
                'productos_con_stock_bajo': 0,
            }
        
        total_unidades = sum(p.stock for p in productos)
        valor_total = sum(p.valor_total for p in productos)
        precio_promedio = sum(p.precio for p in productos) / len(productos)
        
        agotados = [p for p in productos if p.agotado]
        stock_bajo = [p for p in productos if p.stock_bajo]
        disponibles = [p for p in productos if not p.agotado and not p.stock_bajo]
        
        return {
            'total_productos': len(productos),
            'total_unidades': total_unidades,
            'valor_total': round(valor_total, 2),
            'stock_promedio': round(total_unidades / len(productos), 2),
            'precio_promedio': round(precio_promedio, 2),
            'productos_disponibles': len(disponibles),
            'productos_agotados': len(agotados),
            'productos_con_stock_bajo': len(stock_bajo),
        }
    
    def obtener_alertas(self) -> Dict[str, Any]:
        """
        Obtener alertas de productos.
        
        RESPONSABILIDADES: 1
        • Identificar productos en alerta (bajo stock o agotados)
        
        Returns:
            dict: Alertas con:
              • total_productos: Total en catálogo
              • productos_con_stock_bajo: Cantidad
              • productos_agotados: Cantidad
              • total_alertas: suma de ambas
              • lista_stock_bajo: Objetos de productos
              • lista_agotados: Objetos de productos
        """
        productos = self.repository.listar()
        
        stock_bajo = [p for p in productos if p.stock_bajo]
        agotados = [p for p in productos if p.agotado]
        
        return {
            'total_productos': len(productos),
            'productos_con_stock_bajo': len(stock_bajo),
            'productos_agotados': len(agotados),
            'total_alertas': len(stock_bajo) + len(agotados),
            'lista_stock_bajo': [p.to_dict() for p in stock_bajo],
            'lista_agotados': [p.to_dict() for p in agotados],
        }
    
    def obtener_historial(
        self,
        producto_id: Optional[str] = None,
        limite: int = 100,
    ) -> Dict[str, Any]:
        """
        Obtener historial de movimientos.
        
        RESPONSABILIDADES: 1
        • Traer movimientos filtrados opcionalmente por producto
        
        Args:
            producto_id: ID opcional para filtrar por producto
            limite: Máximo de registros (default 100)
        
        Returns:
            dict: Historial con:
              • total_registros: Cantidad de movimientos
              • producto_id_filtro: Filtro aplicado (o None)
              • movimientos: Lista de registros
        """
        movimientos = self.repository.obtener_historial(producto_id, limite)
        
        return {
            'total_registros': len(movimientos),
            'producto_id_filtro': producto_id,
            'movimientos': movimientos,
        }
    
    def obtener_productos_mayor_stock(self, limite: int = 5) -> List[Dict[str, Any]]:
        """
        Obtener productos con mayor stock.
        
        RESPONSABILIDADES: 1
        • Ordenar por stock descendente
        
        Args:
            limite: Cantidad máxima de productos (default 5)
        
        Returns:
            list: Top N productos ordenados por stock descendente
        """
        productos = self.repository.listar()
        ordenados = sorted(productos, key=lambda p: p.stock, reverse=True)
        return [p.to_dict() for p in ordenados[:limite]]
    
    def obtener_productos_menor_stock(self, limite: int = 5) -> List[Dict[str, Any]]:
        """
        Obtener productos con menor stock.
        
        RESPONSABILIDADES: 1
        • Ordenar por stock ascendente
        
        Args:
            limite: Cantidad máxima de productos (default 5)
        
        Returns:
            list: Bottom N productos ordenados por stock ascendente
        """
        productos = self.repository.listar()
        ordenados = sorted(productos, key=lambda p: p.stock)
        return [p.to_dict() for p in ordenados[:limite]]
    
    def obtener_valor_total_inventario(self) -> float:
        """
        Obtener valor total del inventario.
        
        RESPONSABILIDADES: 1
        • Sumar valuación de todo el inventario
        
        Returns:
            float: Valor total (∑ precio * stock)
        
        Fórmula: Σ (producto.precio * producto.stock) para todos los productos
        """
        productos = self.repository.listar()
        return sum(p.valor_total for p in productos)
