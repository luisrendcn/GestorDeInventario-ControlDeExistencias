"""
facade/
-------
Patrón estructural: Facade (Fachada).

Expone una interfaz unificada y simple para acceder a múltiples subsistemas.

Componentes:
    - SistemaInventarioFacade: clase fachada que coordina:
      * ProductoManagementMixin: gestión de productos
      * TransaccionesMixin: ventas y compras
      * EstadisticasMixin: historial, logs y estadísticas

Los controladores interactúan SOLO con SistemaInventarioFacade.
"""

from .facade import SistemaInventarioFacade

__all__ = ['SistemaInventarioFacade']
