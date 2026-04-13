"""
╔════════════════════════════════════════════════════════════════════════════╗
║              ARCHIVO: core/models/producto/to_dict.py                     ║
║              RESPONSABILIDAD: Convertir a diccionario                     ║
╚════════════════════════════════════════════════════════════════════════════╝

🎯 ÚNICA RESPONSABILIDAD:
   Convertir Producto a diccionario (para API/JSON).
   
💡 USO:
   • Serialización JSON en endpoints REST
   • Respuestas HTTP
"""

from typing import Dict, Any


class ToDictMixin:
    """
    Mixin que agrega método to_dict a Producto.
    
    RESPONSABILIDAD: 1
    • Convertir a diccionario para serialización JSON
    
    Requiere atributos:
        • self.id, nombre, precio, stock, stock_minimo, descripcion
        • self.created_at, updated_at
        • Propiedades: valor_total, stock_bajo, agotado
    """
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convertir a diccionario (para API/JSON).
        
        Returns:
            Diccionario con todos los datos e propiedades computadas
        """
        return {
            'id': self.id,
            'nombre': self.nombre,
            'precio': self.precio,
            'stock': self.stock,
            'stock_minimo': self.stock_minimo,
            'descripcion': self.descripcion,
            'valor_total': self.valor_total,
            'stock_bajo': self.stock_bajo,
            'agotado': self.agotado,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }
