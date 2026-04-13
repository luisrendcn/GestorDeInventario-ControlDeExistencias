"""
╔════════════════════════════════════════════════════════════════════════════╗
║   ARCHIVO: producto_repository/crear.py                                   ║
║   RESPONSABILIDAD: Crear nuevo producto en la BD                          ║
╚════════════════════════════════════════════════════════════════════════════╝

🎯 ÚNICA RESPONSABILIDAD:
   Insertar un nuevo producto mediante INSERT INTO.
"""


class CrearMixin:
    """
    Mixin que agrega método para crear productos.
    
    RESPONSABILIDAD: 1
    • Persistir nuevo producto en BD
    
    Requiere atributos:
        • self.executor (QueryExecutor)
    """
    
    def crear(self, producto) -> bool:
        """
        📝 Crear un nuevo producto en la BD.
        
        Ejecuta INSERT INTO productos.
        
        Args:
            producto: Objeto Producto con datos completos
        
        Returns:
            bool: True si INSERT fue exitoso (rows > 0)
        
        Flujo:
            1. Construir query INSERT con placeholders
            2. Extraer valores del objeto Producto
            3. Ejecutar mediante QueryExecutor.ejecutar()
            4. Retornar True si rows_affected > 0
        """
        query = """
            INSERT INTO productos 
            (id, nombre, precio, stock, stock_minimo, descripcion, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            producto.id,
            producto.nombre,
            producto.precio,
            producto.stock,
            producto.stock_minimo,
            producto.descripcion,
            producto.created_at,
            producto.updated_at,
        )
        return self.executor.ejecutar(query, params) > 0
