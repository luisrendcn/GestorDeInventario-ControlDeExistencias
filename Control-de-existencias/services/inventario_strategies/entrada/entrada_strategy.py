"""
Estrategia de ENTRADA de stock (suma sin validación máxima).
"""

from infrastructure.repositories import ProductoRepository, MovimientoRepository
from services.base_service import Service, ProductoValidator
from services.inventario_strategies.entrada.validar_entrada import validar_entrada, validar_schema
from services.inventario_strategies.entrada.sumar_stock import sumar_stock
from services.inventario_strategies.entrada.registrar_entrada import registrar_entrada


class EntradaStrategy(Service):
    """
    Estrategia de ENTRADA de stock.
    
    RESPONSABILIDAD (1):
      1️⃣  Orquestar el proceso completo de entrada
    
    Caso de uso: Recepción de compras, devoluciones de clientes
    
    El proceso consiste en:
      1. Validar datos
      2. Obtener el producto
      3. Sumar stock
      4. Registrar en BD
    """
    
    def __init__(self, producto_repo: ProductoRepository, movimiento_repo: MovimientoRepository):
        """Inyectar repositorios."""
        super().__init__(producto_repo)
        self.movimiento_repo = movimiento_repo
    
    def ejecutar(self, producto_id: str, cantidad: int, motivo: str = 'Entrada') -> dict:
        """
        Ejecutar entrada de stock.
        
        Orquesta: validación → obtención → operación → persistencia
        
        Returns:
            dict con detalles de la entrada
        """
        # 1. VALIDAR
        validar_entrada(cantidad)
        validar_schema(producto_id, cantidad, motivo)
        
        # 2. OBTENER PRODUCTO
        producto = ProductoValidator.validar_existe(self.repository, producto_id)
        stock_anterior = producto.stock
        
        # 3. SUMAR STOCK
        sumar_stock(producto, cantidad)
        
        # 4. REGISTRAR
        registrar_entrada(
            producto=producto,
            producto_id=producto_id,
            cantidad=cantidad,
            stock_anterior=stock_anterior,
            motivo=motivo,
            producto_repo=self.repository,
            movimiento_repo=self.movimiento_repo
        )
        
        # 5. RETORNAR RESULTADO
        return {
            'producto_id': producto_id,
            'tipo': 'ENTRADA',
            'cantidad': cantidad,
            'stock_anterior': stock_anterior,
            'stock_nuevo': producto.stock,
            'motivo': motivo or 'Entrada'
        }
