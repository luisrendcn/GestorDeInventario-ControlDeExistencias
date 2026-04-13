"""
╔════════════════════════════════════════════════════════════════════════════╗
║                  ARCHIVO: services/base_service.py                        ║
║                  FUNCIÓN: Clases base con SRP perfecto                   ║
╚════════════════════════════════════════════════════════════════════════════╝

📋 RESPONSABILIDAD DEL ARCHIVO (2 CLASES):
   1. Service base para inyección de dependencias
   2. Validador de productos

═════════════════════════════════════════════════════════════════════════════

📦 CLASES:

┌─ class Service (RESPONSABILIDAD: 1)
│  └─ Responsabilidad: Almacenar repositorio inyectado
│     └─ __init__(repository) - almacenar referencia
│
┌─ class ProductoValidator (RESPONSABILIDAD: 1)
│  └─ Responsabilidad: Validar existencia de productos
│     └─ validar_existe(repository, producto_id) - verificar en BD
│
🔄 INYECCIÓN DE DEPENDENCIAS:
   Todos los servicios reciben el repositorio en __init__
   Permite testear con mocks y cambiar implementación fácilmente
"""

from infrastructure.repositories import ProductoRepository
from core.exceptions import ProductoNoEncontrado


class Service:
    """
    Clase base para servicios.
    
    RESPONSABILIDAD: 1
    • Almacenar repositorio inyectado
    """
    
    def __init__(self, repository: ProductoRepository):
        """
        Inicializar con repositorio.
        
        Args:
            repository: Instancia de ProductoRepository inyectada
        """
        self.repository = repository


class ProductoValidator:
    """
    Validador de existencia de productos.
    
    RESPONSABILIDAD: 1
    • Validar que producto existe en BD
    """
    
    @staticmethod
    def validar_existe(repository: ProductoRepository, producto_id: str):
        """
        Validar que el producto existe.
        
        RESPONSABILIDAD: 1
        • Verificar que el producto existe en BD
        
        Args:
            repository: Repositorio a consultar
            producto_id: ID del producto a validar
        
        Returns:
            Producto: Objeto del producto si existe
        
        Raises:
            ProductoNoEncontrado: Si el producto no existe
        
        Usado por:
          • ProductoService.obtener_producto()
          • InventarioService.entrada_stock()
          • InventarioService.salida_stock()
          • etc.
        """
        producto = repository.obtener(producto_id)
        if not producto:
            raise ProductoNoEncontrado(f"Producto con ID '{producto_id}' no encontrado")
        return producto
