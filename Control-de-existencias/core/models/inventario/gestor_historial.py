"""
╔════════════════════════════════════════════════════════════════════════════╗
║                  ARCHIVO: core/models/inventario/gestor_historial.py      ║
║                  RESPONSABILIDAD: Orquestar auditoría de movimientos      ║
╚════════════════════════════════════════════════════════════════════════════╝

🎯 ÚNICA RESPONSABILIDAD:
   Coordinar los mixins de registrar y obtener historial.
   
💡 COMPONE:
   • RegistrarMovimientoMixin - Crear entradas de auditoría
   • ObtenerHistorialMixin - Recuperar movimientos
"""

from core.models.inventario.registrar_movimiento import RegistrarMovimientoMixin
from core.models.inventario.obtener_historial import ObtenerHistorialMixin


class GestorHistorialMixin(RegistrarMovimientoMixin, ObtenerHistorialMixin):
    """
    Mixin orquestador de gestión de historial.
    
    RESPONSABILIDAD: 1
    • Combinar mixins de registro y consulta de historial
    
    Submixins:
        • RegistrarMovimientoMixin - registrar_movimiento()
        • ObtenerHistorialMixin - obtener_historial()
    
    Requiere atributo:
        • self._historial (list)
    """
    pass
