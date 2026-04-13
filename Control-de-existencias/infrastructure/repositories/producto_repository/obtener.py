"""
╔════════════════════════════════════════════════════════════════════════════╗
║   ARCHIVO: producto_repository/obtener.py                                 ║
║   RESPONSABILIDAD: Obtener producto por ID                                ║
╚════════════════════════════════════════════════════════════════════════════╝

🎯 ÚNICA RESPONSABILIDAD:
   Leer un producto específico desde BD por su ID.
"""

from typing import Optional
from core.models import Producto


class ObtenerMixin:
    """
    Mixin que agrega método para obtener un producto.
    
    RESPONSABILIDAD: 1
    • Recuperar un producto específico
    
    Requiere atributos:
        • self.reader (QueryReader)
    """
    
    def obtener(self, id: str) -> Optional[Producto]:
        """
        🔍 Obtener UN producto por su ID.
        
        Ejecuta SELECT * FROM productos WHERE id = ?.
        
        Args:
            id: ID único del producto
        
        Returns:
            Optional[Producto]: Objeto Producto si existe, None si no
        
        Flujo:
            1. Ejecutar SELECT con filtro ID
            2. Si hay row, convertir con Producto.from_row()
            3. Si no hay row, retornar None
        """
        row = self.reader.fetchone(
            "SELECT * FROM productos WHERE id = ?",
            (id,)
        )
        if row:
            return Producto.from_row(row)
        return None
