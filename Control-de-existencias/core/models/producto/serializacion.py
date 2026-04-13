"""
╔════════════════════════════════════════════════════════════════════════════╗
║              ARCHIVO: core/models/producto/serializacion.py               ║
║              RESPONSABILIDAD: Orquestar conversiones                      ║
╚════════════════════════════════════════════════════════════════════════════╝

🎯 ÚNICA RESPONSABILIDAD:
   Combinar los mixins de serialización/desserialización.
   
💡 COMPONE:
   • ToDictMixin - Convertir a diccionario (→ JSON)
   • ToTupleMixin - Convertir a tupla (→ BD)
   • FromDictMixin - Crear desde diccionario (← JSON)
   • FromRowMixin - Crear desde fila BD (← BD)
"""

from core.models.producto.to_dict import ToDictMixin
from core.models.producto.to_tuple import ToTupleMixin
from core.models.producto.from_dict import FromDictMixin
from core.models.producto.from_row import FromRowMixin


class SerializacionMixin(ToDictMixin, ToTupleMixin, FromDictMixin, FromRowMixin):
    """
    Mixin orquestador de conversiones.
    
    RESPONSABILIDAD: 1
    • Combinar mixins de serialización bidireccional
    
    Submixins:
        • ToDictMixin - to_dict()
        • ToTupleMixin - to_tuple()
        • FromDictMixin - from_dict()
        • FromRowMixin - from_row()
    
    Requiere atributos:
        • self.id, nombre, precio, stock, stock_minimo, descripcion
        • self.created_at, updated_at
        • Propiedades: valor_total, stock_bajo, agotado
    """
    pass
