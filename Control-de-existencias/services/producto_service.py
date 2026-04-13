"""
╔════════════════════════════════════════════════════════════════════════════╗
║                  ARCHIVO: services/producto_service.py                    ║
║                  FUNCIÓN: Servicios CRUD de productos                     ║
╚════════════════════════════════════════════════════════════════════════════╝

📋 RESPONSABILIDAD DEL ARCHIVO:
   Implementar la lógica de negocio para todas las operaciones CRUD
   (Create, Read, Update, Delete) de productos.

🎯 FUNCIONALIDADES:
   ✓ Crear productos
   ✓ Obtener un producto
   ✓ Listar todos los productos
   ✓ Actualizar producto
   ✓ Eliminar producto
   ✓ Buscar productos por nombre

═════════════════════════════════════════════════════════════════════════════

📦 CLASES:

┌─ class ProductoService (RESPONSABILIDADES: 5)
│  ├─ Responsabilidad 1: Crear productos
│  │  └─ crear_producto(datos) - validar, crear, persistir
│  │
│  ├─ Responsabilidad 2: Leer/obtener productos
│  │  ├─ obtener_producto(id) - traer un producto
│  │  └─ listar_productos() - traer todos
│  │
│  ├─ Responsabilidad 3: Actualizar productos
│  │  └─ actualizar_producto(id, datos) - modificar
│  │
│  ├─ Responsabilidad 4: Eliminar productos
│  │  └─ eliminar_producto(id) - borrar
│  │
│  └─ Responsabilidad 5: Búsqueda
│     └─ buscar_por_nombre(nombre) - filtrar by nombre
│
🔗 HERENCIA:
   ProductoService extends BaseService
   • Hereda: self.repository, validar_producto_existe()

🔄 FLUJO:
   API Handler → ProductoService.método() → validate → repository → DB
   ↓ (error)                                        → exception → handler
"""

from typing import Dict, List, Any
from core.models import Producto
from core.schemas import CrearProductoSchema
from core.exceptions import DatosInvalidos
from .base_service import Service


class ProductoService(Service):
    """
    Servicios de CRUD para productos.
    
    RESPONSABILIDADES: 5
    1. Crear productos (crear_producto)
    2. Leer productos (obtener_producto, listar_productos)
    3. Actualizar productos (actualizar_producto)
    4. Eliminar productos (eliminar_producto)
    5. Búsqueda (buscar_por_nombre)
    """
    
    def crear_producto(self, datos: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crear un nuevo producto.
        
        RESPONSABILIDADES: 1
        • Validar datos, crear objeto, persistir en BD
        
        Args:
            datos: Diccionario con: id, nombre, precio, stock, stock_minimo, descripcion
        
        Returns:
            dict: Producto creado en formato dict
        
        Raises:
            DatosInvalidos: Si algún dato es inválido
        
        Flujo:
            1. Validar schema (CrearProductoSchema.validar())
            2. Crear objeto Producto
            3. Persistir en repositorio
            4. Retornar como diccionario
        """
        # Validar schema
        schema = CrearProductoSchema(
            id=datos.get('id'),
            nombre=datos.get('nombre'),
            precio=datos.get('precio'),
            stock=datos.get('stock'),
            stock_minimo=datos.get('stock_minimo', 5),
            descripcion=datos.get('descripcion', ''),
        )
        schema.validar()
        
        # Crear producto
        producto = Producto.from_dict(datos)
        
        # Persistir
        self.repository.crear(producto)
        
        # Retornar
        return producto.to_dict()
    
    def obtener_producto(self, producto_id: str) -> Dict[str, Any]:
        """
        Obtener un producto.
        
        RESPONSABILIDADES: 1
        • Validar existencia y retornar
        
        Args:
            producto_id: ID del producto
        
        Returns:
            dict: Producto en formato dict
        
        Raises:
            ProductoNoEncontrado: Si el producto no existe
        """
        producto = self.validar_producto_existe(producto_id)
        return producto.to_dict()
    
    def listar_productos(self) -> List[Dict[str, Any]]:
        """
        Listar todos los productos.
        
        RESPONSABILIDADES: 1
        • Traer todos y convertir a lista de dicts
        
        Returns:
            list: Lista de productos en formato dict
        """
        productos = self.repository.listar()
        return [p.to_dict() for p in productos]
    
    def actualizar_producto(self, producto_id: str, datos: Dict[str, Any]) -> Dict[str, Any]:
        """
        Actualizar producto.
        
        RESPONSABILIDADES: 1
        • Validar, actualizar, persistir
        """
        producto = self.validar_producto_existe(producto_id)
        
        # Actualizar atributos
        if 'nombre' in datos:
            producto.nombre = datos['nombre']
        if 'precio' in datos:
            producto.precio = datos['precio']
        if 'stock_minimo' in datos:
            producto.stock_minimo = datos['stock_minimo']
        if 'descripcion' in datos:
            producto.descripcion = datos['descripcion']
        
        # Persistir
        self.repository.actualizar(producto)
        return producto.to_dict()
    
    def eliminar_producto(self, producto_id: str) -> bool:
        """
        Eliminar un producto.
        
        RESPONSABILIDADES: 1
        • Validar existencia y eliminar
        
        Args:
            producto_id: ID del producto
        
        Returns:
            bool: True si se eliminó
        
        Raises:
            ProductoNoEncontrado: Si el producto no existe
        """
        self.validar_producto_existe(producto_id)
        return self.repository.eliminar(producto_id)
    
    def buscar_por_nombre(self, nombre: str) -> List[Dict[str, Any]]:
        """
        Buscar productos por nombre.
        
        RESPONSABILIDADES: 1
        • Buscar case-insensitive
        
        Args:
            nombre: Cadena de búsqueda
        
        Returns:
            list: Productos que coinciden
        """
        productos = self.repository.listar()
        resultado = [
            p for p in productos 
            if nombre.lower() in p.nombre.lower()
        ]
        return [p.to_dict() for p in resultado]
