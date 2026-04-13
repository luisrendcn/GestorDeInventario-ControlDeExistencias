"""
╔════════════════════════════════════════════════════════════════════════════╗
║              ARCHIVO: services/producto_services.py                       ║
║              FUNCIÓN: Servicios CRUD de Productos (SRP perfecto)         ║
╚════════════════════════════════════════════════════════════════════════════╝

📋 RESPONSABILIDAD DEL ARCHIVO (5 CLASES):
   Cada clase tiene EXACTAMENTE 1 responsabilidad para cumplir SRP perfecto

═════════════════════════════════════════════════════════════════════════════

📦 CLASES:

┌─ class CrearProductoService (RESPONSABILIDAD: 1)
│  └─ Responsabilidad: Crear nuevos productos
│
┌─ class ObtenerProductoService (RESPONSABILIDAD: 1)
│  └─ Responsabilidad: Obtener un producto por ID
│
┌─ class ListarProductosService (RESPONSABILIDAD: 1)
│  └─ Responsabilidad: Listar todos los productos
│
┌─ class ActualizarProductoService (RESPONSABILIDAD: 1)
│  └─ Responsabilidad: Actualizar producto existente
│
┌─ class EliminarProductoService (RESPONSABILIDAD: 1)
│  └─ Responsabilidad: Eliminar producto
│
┌─ class BuscarProductoService (RESPONSABILIDAD: 1)
│  └─ Responsabilidad: Buscar productos por nombre
"""

from core.schemas import CrearProductoSchema, ActualizarProductoSchema
from core.exceptions import ProductoNoEncontrado
from infrastructure.repositories import ProductoRepository
from services.base_service import Service, ProductoValidator


class CrearProductoService(Service):
    """
    Servicio para crear nuevos productos.
    
    RESPONSABILIDAD (1):
      1️⃣  Crear un producto en la BD
    
    Flujo:
      1. Validar schema
      2. Crear objeto Producto
      3. Persistir en repositorio
      4. Retornar producto creado
    """
    
    def crear(self, data: dict):
        """
        Crear un nuevo producto.
        
        Args:
            data: Diccionario con id, nombre, precio, stock, stock_minimo
        
        Returns:
            dict: Producto creado como diccionario
        
        Raises:
            DatosInvalidos: Si validación falla
        """
        schema = CrearProductoSchema(**data)
        schema.validar()
        
        producto = schema.to_producto()
        self.repository.crear(producto)
        
        return producto.to_dict()


class ObtenerProductoService(Service):
    """
    Servicio para obtener un producto por ID.
    
    RESPONSABILIDAD (1):
      1️⃣  Obtener productoexistente por ID
    
    Flujo:
      1. Validar que existe
      2. Obtener del repositorio
      3. Retornar como diccionario
    """
    
    def obtener(self, producto_id: str):
        """
        Obtener un producto por su ID.
        
        Args:
            producto_id: ID del producto
        
        Returns:
            dict: Producto encontrado
        
        Raises:
            ProductoNoEncontrado: Si no existe
        """
        producto = ProductoValidator.validar_existe(self.repository, producto_id)
        return producto.to_dict()


class ListarProductosService(Service):
    """
    Servicio para listar todos los productos.
    
    RESPONSABILIDAD (1):
      1️⃣  Listar todos los productos
    
    Flujo:
      1. Obtener todos del repositorio
      2. Convertir a lista de diccionarios
      3. Retornar
    """
    
    def listar(self):
        """
        Listar todos los productos.
        
        Returns:
            list: Lista de todos los productos
        """
        productos = self.repository.listar()
        return [p.to_dict() for p in productos]


class ActualizarProductoService(Service):
    """
    Servicio para actualizar un producto.
    
    RESPONSABILIDAD (1):
      1️⃣  Actualizar producto existente
    
    Flujo:
      1. Validar que existe
      2. Validar schema
      3. Actualizar en repositorio
      4. Retornar producto actualizado
    """
    
    def actualizar(self, producto_id: str, data: dict):
        """
        Actualizar un producto existente.
        
        Args:
            producto_id: ID del producto
            data: Diccionario con campos a actualizar
        
        Returns:
            dict: Producto actualizado
        
        Raises:
            ProductoNoEncontrado: Si no existe
            DatosInvalidos: Si validación falla
        """
        # Validar que existe
        producto = ProductoValidator.validar_existe(self.repository, producto_id)
        
        # Validar schema
        schema = ActualizarProductoSchema(**data)
        schema.validar()
        
        # Actualizar campo a campo si está en data
        if 'nombre' in data:
            producto.nombre = data['nombre']
        if 'precio' in data:
            producto.precio = float(data['precio'])
        if 'stock' in data:
            producto.stock = int(data['stock'])
        if 'stock_minimo' in data:
            producto.stock_minimo = int(data['stock_minimo'])
        if 'descripcion' in data:
            producto.descripcion = data['descripcion']
        
        # Persistir
        self.repository.actualizar(producto)
        
        return producto.to_dict()


class EliminarProductoService(Service):
    """
    Servicio para eliminar un producto.
    
    RESPONSABILIDAD (1):
      1️⃣  Eliminar producto existente
    
    Flujo:
      1. Validar que existe
      2. Eliminar del repositorio
      3. Retornar confirmación
    """
    
    def eliminar(self, producto_id: str):
        """
        Eliminar un producto.
        
        Args:
            producto_id: ID del producto a eliminar
        
        Returns:
            dict: Confirmación de eliminación
        
        Raises:
            ProductoNoEncontrado: Si no existe
        """
        # Validar que existe
        ProductoValidator.validar_existe(self.repository, producto_id)
        
        # Eliminar
        success = self.repository.eliminar(producto_id)
        
        return {
            'mensaje': 'Producto eliminado exitosamente',
            'producto_id': producto_id,
            'success': success
        }


class BuscarProductoService(Service):
    """
    Servicio para buscar productos por nombre.
    
    RESPONSABILIDAD (1):
      1️⃣  Buscar productos por nombre
    
    Flujo:
      1. Obtener todos los productos
      2. Filtrar por nombre (case-insensitive)
      3. Retornar resultados
    """
    
    def buscar_por_nombre(self, nombre: str):
        """
        Buscar productos por nombre (búsqueda parcial).
        
        Args:
            nombre: Parte del nombre a buscar
        
        Returns:
            list: Productos que coinciden
        """
        productos = self.repository.listar()
        nombre_lower = nombre.lower()
        
        resultados = [
            p.to_dict() for p in productos
            if nombre_lower in p.nombre.lower()
        ]
        
        return resultados
