"""
Persistencia: registrar movimiento de entrada y actualizar stock.
"""

from infrastructure.repositories import ProductoRepository, MovimientoRepository
from core.models import Producto


def registrar_entrada(
    producto: Producto,
    producto_id: str,
    cantidad: int,
    stock_anterior: int,
    motivo: str,
    producto_repo: ProductoRepository,
    movimiento_repo: MovimientoRepository
) -> None:
    """
    Persistir la entrada: actualizar producto y registrar movimiento.
    
    RESPONSABILIDAD ÚNICA: Guardar cambios en repositorios.
    """
    # Actualizar producto en BD
    producto_repo.actualizar(producto)
    
    # Registrar movimiento en historial
    movimiento_repo.registrar_movimiento(
        producto_id=producto_id,
        tipo='ENTRADA',
        cantidad=cantidad,
        stock_anterior=stock_anterior,
        stock_nuevo=producto.stock,
        descripcion=motivo or 'Entrada'
    )
