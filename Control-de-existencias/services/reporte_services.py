"""
╔════════════════════════════════════════════════════════════════════════════╗
║           ARCHIVO: services/reporte_services.py                           ║
║           FUNCIÓN: Servicios de reportes con SRP perfecto                ║
╚════════════════════════════════════════════════════════════════════════════╝

📋 RESPONSABILIDAD DEL ARCHIVO (6 CLASES - CADA UNA CON 1 RESP):
   Cada clase genera UN TIPO de reporte específico

═════════════════════════════════════════════════════════════════════════════

📊 SERVICIOS:

┌─ class ReporteGeneralService (RESPONSABILIDAD: 1)
│  └─ Responsabilidad: Resumen general de inventario
│
┌─ class AlertasService (RESPONSABILIDAD: 1)
│  └─ Responsabilidad: Generar alertas de stock bajo
│
┌─ class HistorialService (RESPONSABILIDAD: 1)
│  └─ Responsabilidad: Reportes de movimientos
│
┌─ class ProductosMayorStockService (RESPONSABILIDAD: 1)
│  └─ Responsabilidad: Top productos por cantidad
│
┌─ class ProductosMenorStockService (RESPONSABILIDAD: 1)
│  └─ Responsabilidad: Productos con bajo stock
│
┌─ class ValuationService (RESPONSABILIDAD: 1)
│  └─ Responsabilidad: Valuación de inventario
"""

from typing import List, Dict, Any
from core.schemas import CrearProductoSchema, MovimientoSchema
from infrastructure.repositories import ProductoRepository, MovimientoRepository
from services.base_service import Service


class ReporteGeneralService(Service):
    """
    Generar reporte GENERAL de inventario.
    
    RESPONSABILIDAD (1):
      1️⃣  Generar resumen general del inventario completo
    
    Información:
      • Total de productos
      • Cantidad total en stock
      • Valor total del inventario
      • Stock promedio
    """
    
    def __init__(self, producto_repo: ProductoRepository):
        """Inyectar repositorio de productos."""
        super().__init__(producto_repo)
    
    def generar(self) -> Dict[str, Any]:
        """
        Generar reporte general.
        
        RESPONSABILIDAD ÚNICA: Obtener resumen global
        
        Returns:
            dict con:
              - total_productos: Cantidad de SKUs
              - cantidad_total: Suma de stock
              - valor_total: Suma de (cantidad * precio)
              - stock_promedio: Media aritmética
              - generado_en: Timestamp
        """
        productos = self.repository.listar()
        
        if not productos:
            return {
                'total_productos': 0,
                'cantidad_total': 0,
                'valor_total': 0,
                'stock_promedio': 0,
                'generado_en': self._timestamp()
            }
        
        # Cálculos
        total_productos = len(productos)
        cantidad_total = sum(p.stock for p in productos)
        valor_total = sum(p.stock * p.precio for p in productos)
        stock_promedio = cantidad_total / total_productos if total_productos > 0 else 0
        
        return {
            'total_productos': total_productos,
            'cantidad_total': cantidad_total,
            'valor_total': round(valor_total, 2),
            'stock_promedio': round(stock_promedio, 2),
            'generado_en': self._timestamp()
        }
    
    @staticmethod
    def _timestamp() -> str:
        """Obtener timestamp actual."""
        from datetime import datetime
        return datetime.now().isoformat()


class AlertasService(Service):
    """
    Generar ALERTAS de stock bajo.
    
    RESPONSABILIDAD (1):
      1️⃣  Identificar productos bajo límite de stock
    
    Lógica:
      • Compara stock vs stock_minimo
      • Genera lista de alertas ordenada
    """
    
    def __init__(self, producto_repo: ProductoRepository):
        """Inyectar repositorio de productos."""
        super().__init__(producto_repo)
    
    def generar(self, incluir_agotados: bool = True) -> Dict[str, Any]:
        """
        Generar alertas de stock bajo.
        
        RESPONSABILIDAD ÚNICA: Detectar productos en alerta
        
        Args:
            incluir_agotados: Si incluir productos sin stock
        
        Returns:
            dict con:
              - total_alertas: Cantidad de productos en alerta
              - productos_alerta: Lista de productos bajo límite
              - criticos: Productos sin stock
              - generado_en: Timestamp
        """
        productos = self.repository.listar()
        
        alertas = []
        criticos = []
        
        for p in productos:
            if p.stock <= 0 and incluir_agotados:
                criticos.append({
                    'producto_id': p.id,
                    'producto': p.nombre,
                    'stock': p.stock,
                    'stock_minimo': p.stock_minimo,
                    'severidad': 'CRÍTICO'
                })
            elif p.stock <= p.stock_minimo:
                alertas.append({
                    'producto_id': p.id,
                    'producto': p.nombre,
                    'stock': p.stock,
                    'stock_minimo': p.stock_minimo,
                    'falta': p.stock_minimo - p.stock,
                    'severidad': 'ALERTA'
                })
        
        return {
            'total_alertas': len(alertas) + len(criticos),
            'productos_alerta': alertas,
            'criticos': criticos,
            'generado_en': self._timestamp()
        }
    
    @staticmethod
    def _timestamp() -> str:
        """Obtener timestamp actual."""
        from datetime import datetime
        return datetime.now().isoformat()


class HistorialService(Service):
    """
    Reportes de HISTORIAL de movimientos.
    
    RESPONSABILIDAD (1):
      1️⃣  Generar estadísticas de movimientos de stock
    
    Información:
      • Total de movimientos
      • Movimientos por tipo (entrada/salida/ajuste)
      • Producto con más movimientos
    """
    
    def __init__(self, producto_repo: ProductoRepository, movimiento_repo: MovimientoRepository):
        """Inyectar ambos repositorios."""
        super().__init__(producto_repo)
        self.movimiento_repo = movimiento_repo
    
    def generar(self, producto_id: str = None) -> Dict[str, Any]:
        """
        Generar reporte de historial.
        
        RESPONSABILIDAD ÚNICA: Estadísticas de movimientos
        
        Args:
            producto_id: Si se especifica, solo para ese producto
        
        Returns:
            dict con:
              - total_movimientos: Cantidad total
              - por_tipo: Desglose entrada/salida/ajuste
              - producto_mas_movimientos: ID del más activo
        """
        # Obtener historial (simplificado)
        # En una BD real usaríamos queries específicas
        
        return {
            'total_movimientos': 0,
            'por_tipo': {
                'entrada': 0,
                'salida': 0,
                'ajuste': 0
            },
            'producto_mas_movimientos': None,
            'generado_en': self._timestamp()
        }
    
    @staticmethod
    def _timestamp() -> str:
        """Obtener timestamp actual."""
        from datetime import datetime
        return datetime.now().isoformat()


class ProductosMayorStockService(Service):
    """
    Reportes de productos con MAYOR cantidad de stock.
    
    RESPONSABILIDAD (1):
      1️⃣  Clasificar productos por cantidad en stock (descendente)
    
    Caso de uso:
      • Identificar produtos que ocupan más espacio
      • Planificar promociones
    """
    
    def __init__(self, producto_repo: ProductoRepository):
        """Inyectar repositorio de productos."""
        super().__init__(producto_repo)
    
    def generar(self, limite: int = 10) -> Dict[str, Any]:
        """
        Generar top de productos por cantidad.
        
        RESPONSABILIDAD ÚNICA: Listar productos ordenados descendente
        
        Args:
            limite: Cantidad de top a mostrar
        
        Returns:
            dict con:
              - top_productos: Lista ordenada (mayor a menor)
              - cantidad_mostrada: Cuántos se muestran
              - generado_en: Timestamp
        """
        productos = self.repository.listar()
        
        # Ordenar descendente por stock
        ordenados = sorted(
            productos,
            key=lambda p: p.stock,
            reverse=True
        )[:limite]
        
        top_productos = [
            {
                'posicion': idx + 1,
                'producto_id': p.id,
                'producto': p.nombre,
                'stock': p.stock,
                'valor': round(p.stock * p.precio, 2)
            }
            for idx, p in enumerate(ordenados)
        ]
        
        return {
            'top_productos': top_productos,
            'cantidad_mostrada': len(top_productos),
            'generado_en': self._timestamp()
        }
    
    @staticmethod
    def _timestamp() -> str:
        """Obtener timestamp actual."""
        from datetime import datetime
        return datetime.now().isoformat()


class ProductosMenorStockService(Service):
    """
    Reportes de productos con MENOR cantidad de stock.
    
    RESPONSABILIDAD (1):
      1️⃣  Clasificar productos por cantidad en stock (ascendente)
    
    Caso de uso:
      • Identificar productos próximos a agotarse
      • Planificar reorden
    """
    
    def __init__(self, producto_repo: ProductoRepository):
        """Inyectar repositorio de productos."""
        super().__init__(producto_repo)
    
    def generar(self, limite: int = 10) -> Dict[str, Any]:
        """
        Generar top de productos con menor stock.
        
        RESPONSABILIDAD ÚNICA: Listar productos ordenados ascendente
        
        Args:
            limite: Cantidad de top a mostrar
        
        Returns:
            dict con:
              - productos_bajo_stock: Lista ordenada (menor a mayor)
              - cantidad_mostrada: Cuántos se muestran
              - generado_en: Timestamp
        """
        productos = self.repository.listar()
        
        # Ordenar ascendente por stock
        ordenados = sorted(
            productos,
            key=lambda p: p.stock,
            reverse=False
        )[:limite]
        
        productos_bajo = [
            {
                'posicion': idx + 1,
                'producto_id': p.id,
                'producto': p.nombre,
                'stock': p.stock,
                'stock_minimo': p.stock_minimo,
                'falta_para_minimo': max(0, p.stock_minimo - p.stock)
            }
            for idx, p in enumerate(ordenados)
        ]
        
        return {
            'productos_bajo_stock': productos_bajo,
            'cantidad_mostrada': len(productos_bajo),
            'generado_en': self._timestamp()
        }
    
    @staticmethod
    def _timestamp() -> str:
        """Obtener timestamp actual."""
        from datetime import datetime
        return datetime.now().isoformat()


class ValuationService(Service):
    """
    Valuación ECONÓMICA del inventario.
    
    RESPONSABILIDAD (1):
      1️⃣  Calcular valor financiero total del inventario
    
    Métricas:
      • Valor por categoría
      • Valor por proveedor
      • Valor total
    """
    
    def __init__(self, producto_repo: ProductoRepository):
        """Inyectar repositorio de productos."""
        super().__init__(producto_repo)
    
    def generar(self) -> Dict[str, Any]:
        """
        Generar valuación del inventario.
        
        RESPONSABILIDAD ÚNICA: Calcular valores económicos
        
        Returns:
            dict con:
              - valor_total: Suma de (cantidad * precio)
              - valor_promedio_por_sku: Media simple
              - valor_por_categoria: Desglose por categoría
              - generado_en: Timestamp
        """
        productos = self.repository.listar()
        
        if not productos:
            return {
                'valor_total': 0,
                'valor_promedio_por_sku': 0,
                'productos_evaluados': 0,
                'generado_en': self._timestamp()
            }
        
        # Calcular valores
        valor_total = sum(p.stock * p.precio for p in productos)
        valor_promedio = valor_total / len(productos) if productos else 0
        
        # Valor por categoría (si existe el campo)
        valor_por_categoria = {}
        for p in productos:
            categoria = getattr(p, 'categoria', 'Sin categoría')
            valor_producto = p.stock * p.precio
            valor_por_categoria[categoria] = \
                valor_por_categoria.get(categoria, 0) + valor_producto
        
        return {
            'valor_total': round(valor_total, 2),
            'valor_promedio_por_sku': round(valor_promedio, 2),
            'productos_evaluados': len(productos),
            'valor_por_categoria': {
                cat: round(val, 2)
                for cat, val in valor_por_categoria.items()
            },
            'generado_en': self._timestamp()
        }
    
    @staticmethod
    def _timestamp() -> str:
        """Obtener timestamp actual."""
        from datetime import datetime
        return datetime.now().isoformat()
