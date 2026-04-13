"""
╔════════════════════════════════════════════════════════════════════════════╗
║   ARCHIVO: producto_repository/actualizar.py                              ║
║   RESPONSABILIDAD: Actualizar producto existente                          ║
╚════════════════════════════════════════════════════════════════════════════╝

🎯 ÚNICA RESPONSABILIDAD:
   Modificar un producto mediante UPDATE.
"""

from datetime import datetime


class ActualizarMixin:
    """
    Mixin que agrega método para actualizar productos.
    
    RESPONSABILIDAD: 1
    • Modificar un producto existente
    
    Requiere atributos:
        • self.executor (QueryExecutor)
    """
    
    def actualizar(self, producto) -> bool:
        """
        ✏️  Actualizar un producto existente en la BD.
        
        Ejecuta UPDATE productos SET ... WHERE id = ?.
        
        Args:
            producto: Objeto Producto con datos actualizados
        
        Returns:
            bool: True si UPDATE fue exitoso (rows > 0)
        
        Flujo:
            1. Construir query UPDATE para todos los campos
            2. Extraer valores del objeto Producto
            3. Agregar timestamp de updated_at actualizado
            4. Ejecutar mediante QueryExecutor.ejecutar()
        
        Nota: updated_at se asigna a datetime.now() automáticamente
        """
        query = """
            UPDATE productos 
            SET nombre = ?, precio = ?, stock = ?, stock_minimo = ?, 
                descripcion = ?, updated_at = ?
            WHERE id = ?
        """
        params = (
            producto.nombre,
            producto.precio,
            producto.stock,
            producto.stock_minimo,
            producto.descripcion,
            datetime.now(),
            producto.id,
        )
        return self.executor.ejecutar(query, params) > 0
