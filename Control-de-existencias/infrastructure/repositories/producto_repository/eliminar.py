"""
╔════════════════════════════════════════════════════════════════════════════╗
║   ARCHIVO: producto_repository/eliminar.py                                ║
║   RESPONSABILIDAD: Eliminar producto de la BD                             ║
╚════════════════════════════════════════════════════════════════════════════╝

🎯 ÚNICA RESPONSABILIDAD:
   Borrar un producto específico mediante DELETE.
"""


class EliminarMixin:
    """
    Mixin que agrega método para eliminar productos.
    
    RESPONSABILIDAD: 1
    • Eliminar un producto específico
    
    Requiere atributos:
        • self.executor (QueryExecutor)
    """
    
    def eliminar(self, id: str) -> bool:
        """
        🗑️  Eliminar un producto de la BD.
        
        Ejecuta DELETE FROM productos WHERE id = ?.
        
        Args:
            id: ID del producto a eliminar
        
        Returns:
            bool: True si DELETE fue exitoso (rows > 0)
        
        Nota: Eliminación en cascada de movimientos se configura en BD
        """
        return self.executor.ejecutar(
            "DELETE FROM productos WHERE id = ?",
            (id,)
        ) > 0
