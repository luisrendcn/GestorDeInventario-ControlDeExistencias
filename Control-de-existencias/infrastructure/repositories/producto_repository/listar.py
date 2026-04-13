"""
╔════════════════════════════════════════════════════════════════════════════╗
║   ARCHIVO: producto_repository/listar.py                                  ║
║   RESPONSABILIDAD: Listar todos los productos                             ║
╚════════════════════════════════════════════════════════════════════════════╝

🎯 ÚNICA RESPONSABILIDAD:
   Leer todos los productos desde BD.
"""

from typing import List
from core.models import Producto


class ListarMixin:
    """
    Mixin que agrega método para listar productos.
    
    RESPONSABILIDAD: 1
    • Recuperar todos los productos
    
    Requiere atributos:
        • self.reader (QueryReader)
    """
    
    def listar(self) -> List[Producto]:
        """
        📋 Obtener TODOS los productos.
        
        Ejecuta SELECT * FROM productos ORDER BY id.
        
        Returns:
            List[Producto]: Lista de todos los productos (puede estar vacía)
        
        Flujo:
            1. Ejecutar SELECT sin filtro
            2. Convertir cada row a Producto.from_row()
            3. Retornar lista completa
        """
        rows = self.reader.fetchall("SELECT * FROM productos ORDER BY id")
        return [Producto.from_row(row) for row in rows]
