"""
Persistencia: registrar movimiento de ajuste y actualizar stock.
"""

from infrastructure.repositories import ProductoRepository, MovimientoRepository
from core.models import Producto


def registrar_ajuste(
    producto: Producto,
    producto_id: str,
    stock_anterior: int,
    stock_nuevo: int,
    motivo: str,
    producto_repo: ProductoRepository,
    movimiento_repo: MovimientoRepository
) -> None:
    """
    Persistir el ajuste: actualizar producto y registrar movimiento.
    
    RESPONSABILIDAD ÚNICA: Guardar cambios en repositorios.
    """
    # Calcular cantidad para el historial
    cantidad = abs(stock_nuevo - stock_anterior)
    
    # Actualizar producto en BD
    producto_repo.actualizar(producto)
    
    # Registrar movimiento en historial
    movimiento_repo.registrar_movimiento(
        producto_id=producto_id,
        tipo='AJUSTE',
        cantidad=cantidad,
        stock_anterior=stock_anterior,
        stock_nuevo=stock_nuevo,
        descripcion=motivo or 'Ajuste'
    )
