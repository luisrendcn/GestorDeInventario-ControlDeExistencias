"""
╔════════════════════════════════════════════════════════════════════════════╗
║              ARCHIVO: core/models/producto/from_dict.py                   ║
║              RESPONSABILIDAD: Crear desde diccionario                     ║
╚════════════════════════════════════════════════════════════════════════════╝

🎯 ÚNICA RESPONSABILIDAD:
   Crear Producto a partir de diccionario (factory).
   
💡 USO:
   • Construir desde JSON en requests
   • Desserialización
"""

from typing import Dict, Any


class FromDictMixin:
    """
    Mixin que agrega método de clase from_dict a Producto.
    
    RESPONSABILIDAD: 1
    • Factory para crear instancia desde diccionario
    
    Nota:
        Este es un método de clase (@classmethod), no requiere self
    """
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Producto':
        """
        Crear Producto desde diccionario.
        
        Args:
            data: Diccionario con datos del producto
            
        Returns:
            Instancia nueva de Producto
        """
        return cls(**data)
