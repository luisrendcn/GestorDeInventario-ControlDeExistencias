"""
Estrategia de SALIDA de stock (resta con validación).
"""

from infrastructure.repositories import ProductoRepository, MovimientoRepository
from services.base_service import Service, ProductoValidator
from services.inventario_strategies.salida.validar_salida import (
    validar_salida,
    validar_disponibilidad,
    validar_schema
)
from services.inventario_strategies.salida.restar_stock import restar_stock
from services.inventario_strategies.salida.registrar_salida import registrar_salida


class SalidaStrategy(Service):
    """
    Estrategia de SALIDA de stock.
    
    RESPONSABILIDAD (1):
      1️⃣  Orquestar el proceso completo de salida
    
    Caso de uso: Ventas, retiros de almacén
    
    DIFERENCIA CON ENTRADA: Valida que hay suficiente stock
    
    El proceso consiste en:
      1. Validar datos
      2. Obtener el producto
      3. Validar disponibilidad ← CLAVE
      4. Restar stock
      5. Registrar en BD
    """
    
    def __init__(self, producto_repo: ProductoRepository, movimiento_repo: MovimientoRepository):
        """Inyectar repositorios."""
        super().__init__(producto_repo)
        self.movimiento_repo = movimiento_repo
    
    def ejecutar(self, producto_id: str, cantidad: int, motivo: str = 'Salida') -> dict:
        """
        Ejecutar salida de stock.
        
        Orquesta: validación → obtención → verificación → operación → persistencia
        
        Returns:
            dict con detalles de la salida
        """
        # 1. VALIDAR
        validar_salida(cantidad)
        validar_schema(producto_id, cantidad, motivo)
        
        # 2. OBTENER PRODUCTO
        producto = ProductoValidator.validar_existe(self.repository, producto_id)
        stock_anterior = producto.stock
        
        # 3. VALIDAR DISPONIBILIDAD (DIFERENCIA CLAVE)
        validar_disponibilidad(producto, cantidad)
        
        # 4. RESTAR STOCK
        restar_stock(producto, cantidad)
        
        # 5. REGISTRAR
        registrar_salida(
            producto=producto,
            producto_id=producto_id,
            cantidad=cantidad,
            stock_anterior=stock_anterior,
            motivo=motivo,
            producto_repo=self.repository,
            movimiento_repo=self.movimiento_repo
        )
        
        # 6. RETORNAR RESULTADO
        return {
            'producto_id': producto_id,
            'tipo': 'SALIDA',
            'cantidad': cantidad,
            'stock_anterior': stock_anterior,
            'stock_nuevo': producto.stock,
            'motivo': motivo or 'Salida'
        }
