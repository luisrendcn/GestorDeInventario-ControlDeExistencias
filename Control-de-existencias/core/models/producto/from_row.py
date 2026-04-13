"""
╔════════════════════════════════════════════════════════════════════════════╗
║              ARCHIVO: core/models/producto/from_row.py                    ║
║              RESPONSABILIDAD: Crear desde fila de BD                      ║
╚════════════════════════════════════════════════════════════════════════════╝

🎯 ÚNICA RESPONSABILIDAD:
   Crear Producto a partir de fila de Base de Datos (factory).
   
💡 USO:
   • Mapeo ORM: fila BD → Producto
   • Recuperar registros de BD
"""

from datetime import datetime


class FromRowMixin:
    """
    Mixin que agrega método de clase from_row a Producto.
    
    RESPONSABILIDAD: 1
    • Factory para crear instancia desde fila de BD
    
    Nota:
        Este es un método de clase (@classmethod), no requiere self
    """
    
    @classmethod
    def from_row(cls, row: tuple) -> 'Producto':
        """
        Crear Producto desde fila de BD.
        
        Args:
            row: Tupla con datos en orden: (id, nombre, precio, stock, minimo, desc, created, updated)
            
        Returns:
            Instancia nueva de Producto
        """
        def parse_datetime(dt_str):
            """Convertir string de BD a datetime."""
            if isinstance(dt_str, str):
                try:
                    return datetime.fromisoformat(dt_str)
                except:
                    return datetime.now()
            return dt_str

        return cls(
            id=row[0],
            nombre=row[1],
            precio=row[2],
            stock=row[3],
            stock_minimo=row[4],
            descripcion=row[5],
            created_at=parse_datetime(row[6]),
            updated_at=parse_datetime(row[7]),
        )
