"""
Estrategia de AJUSTE de stock (asigna valor exacto).
"""

from infrastructure.repositories import ProductoRepository, MovimientoRepository
from services.base_service import Service, ProductoValidator
from services.inventario_strategies.ajuste.validar_ajuste import validar_ajuste
from services.inventario_strategies.ajuste.asignar_stock import asignar_stock
from services.inventario_strategies.ajuste.registrar_ajuste import registrar_ajuste


class AjusteStrategy(Service):
    """
    Estrategia de AJUSTE de stock.
    
    RESPONSABILIDAD (1):
      1️⃣  Orquestar el proceso completo de ajuste
    
    Caso de uso: Auditoría física, correcciones por robo/pérdida
    
    DIFERENCIA CON ENTRADA/SALIDA: Asigna valor exacto (no aritmética)
    
    El proceso consiste en:
      1. Validar datos
      2. Obtener el producto
      3. Asignar stock exacto
      4. Registrar en BD
    """
    
    def __init__(self, producto_repo: ProductoRepository, movimiento_repo: MovimientoRepository):
        """Inyectar repositorios."""
        super().__init__(producto_repo)
        self.movimiento_repo = movimiento_repo
    
    def ejecutar(self, producto_id: str, nuevo_stock: int, motivo: str = 'Ajuste') -> dict:
        """
        Ejecutar ajuste de stock.
        
        Orquesta: validación → obtención → asignación → persistencia
        
        Returns:
            dict con detalles del ajuste
        """
        # 1. VALIDAR
        validar_ajuste(nuevo_stock)
        
        # 2. OBTENER PRODUCTO
        producto = ProductoValidator.validar_existe(self.repository, producto_id)
        stock_anterior = producto.stock
        
        # 3. ASIGNAR VALOR EXACTO (NO es aritmética)
        asignar_stock(producto, nuevo_stock)
        
        # 4. REGISTRAR
        registrar_ajuste(
            producto=producto,
            producto_id=producto_id,
            stock_anterior=stock_anterior,
            stock_nuevo=nuevo_stock,
            motivo=motivo,
            producto_repo=self.repository,
            movimiento_repo=self.movimiento_repo
        )
        
        # 5. RETORNAR RESULTADO
        return {
            'producto_id': producto_id,
            'tipo': 'AJUSTE',
            'stock_anterior': stock_anterior,
            'stock_nuevo': nuevo_stock,
            'diferencia': nuevo_stock - stock_anterior,
            'motivo': motivo or 'Ajuste'
        }
