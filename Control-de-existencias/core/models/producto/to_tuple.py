"""
╔════════════════════════════════════════════════════════════════════════════╗
║              ARCHIVO: core/models/producto/to_tuple.py                    ║
║              RESPONSABILIDAD: Convertir a tupla                           ║
╚════════════════════════════════════════════════════════════════════════════╝

🎯 ÚNICA RESPONSABILIDAD:
   Convertir Producto a tupla (para Base de Datos).
   
💡 USO:
   • Inserts/updates en BD
   • Operaciones de persistencia
"""


class ToTupleMixin:
    """
    Mixin que agrega método to_tuple a Producto.
    
    RESPONSABILIDAD: 1
    • Convertir a tupla para persistencia en BD
    
    Requiere atributos:
        • self.id, nombre, precio, stock, stock_minimo, descripcion
        • self.created_at, updated_at
    """
    
    def to_tuple(self) -> tuple:
        """
        Convertir a tupla (para Base de Datos).
        
        Returns:
            Tupla con los datos en orden: (id, nombre, precio, stock, minimo, desc, created, updated)
        """
        return (
            self.id,
            self.nombre,
            self.precio,
            self.stock,
            self.stock_minimo,
            self.descripcion,
            self.created_at,
            self.updated_at,
        )
