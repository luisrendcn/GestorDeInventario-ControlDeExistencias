"""
inventario/inventario.py
========================
Repositorio de inventario organizado con mixins.

Responsabilidad:
    - Coordinar la colección de productos
    - Delegar operaciones a mixins especializados
    - Validar integridad de stock

Aplica:
    - Alta cohesión: gestiona únicamente la colección de productos
    - Bajo acoplamiento: no conoce la lógica de negocio
    - Separación de responsabilidades con mixins
    - SRP: solo es responsable de coordinación y acceso
"""

from typing import Dict, List, Tuple
from .crud import CRUDMixin
from .busqueda import BúsquedaMixin
from .consultas import ConsultasMixin


class Inventario(CRUDMixin, BúsquedaMixin, ConsultasMixin):
    """
    Repositorio en memoria de productos.
    
    Hereda funcionalidad de:
    - CRUDMixin: agregar, obtener, obtener_o_error, eliminar, actualizar_stock_entrada, actualizar_stock_salida
    - BúsquedaMixin: listar_todos, buscar_por_nombre
    - ConsultasMixin: existe, total_productos, valor_total_inventario, productos_con_stock_bajo,
                     obtener_stock_actual, obtener_productos_por_rango_stock
    
    Control de Existencias:
    - Mantiene registro de productos con sus stocks actuales
    - Valida operaciones de entrada y salida
    - Previene stock negativo
    - Proporciona consultas de existencias en tiempo real
    """

    def __init__(self):
        # Usamos un dict para acceso O(1) por ID
        self._productos: Dict[str, 'Producto'] = {}
        # Registro de auditoría de movimientos de stock
        self._historial_movimientos: List[Dict] = []

    def __len__(self) -> int:
        return len(self._productos)

    def __repr__(self) -> str:
        return f"Inventario({len(self._productos)} productos)"

    # Métodos de Control de Existencias
    def registrar_movimiento(self, producto_id: str, tipo: str, cantidad: int) -> None:
        """
        Registra un movimiento de stock (entrada/salida) en el historial de auditoría.
        
        Args:
            producto_id: ID del producto
            tipo: 'entrada' o 'salida'
            cantidad: Cantidad movida
        """
        from datetime import datetime
        
        movimiento = {
            'timestamp': datetime.now(),
            'producto_id': producto_id,
            'tipo': tipo,
            'cantidad': cantidad
        }
        self._historial_movimientos.append(movimiento)

    def obtener_historial(self, producto_id: str = None) -> List[Dict]:
        """
        Obtiene el historial de movimientos.
        
        Args:
            producto_id: Filtra por producto (opcional)
            
        Returns:
            Lista de movimientos de stock
        """
        if producto_id:
            return [m for m in self._historial_movimientos if m['producto_id'] == producto_id]
        return list(self._historial_movimientos)

    def limpiar_historial(self) -> None:
        """Limpia el historial de movimientos."""
        self._historial_movimientos.clear()
