"""
╔════════════════════════════════════════════════════════════════════════════╗
║   ARCHIVO: repositorio_factory/get_producto_repository.py                 ║
║   RESPONSABILIDAD: Factory para crear ProductoRepository                  ║
╚════════════════════════════════════════════════════════════════════════════╝

🎯 ÚNICA RESPONSABILIDAD:
   Factory que crea instantancia singleton de ProductoRepository.
"""


class GetProductoRepositoryMixin:
    """
    Mixin que agrega factory method para ProductoRepository.
    
    RESPONSABILIDAD: 1
    • Crear instancia singleton de ProductoRepository
    
    Requiere:
        • _producto_repo (class variable)
        • DatabaseStore.get_database()
        • ProductoRepository (importar)
    """
    
    @classmethod
    def get_producto_repository(cls):
        """
        🏭 Obtener repositorio de productos (FACTORY METHOD).
        
        Factory que implementa:
          • Validación de precondiciones
          • Instanciación perezosa (lazy initialization)
          • Singleton Pattern (una única instancia)
        
        RESPONSABILIDAD: Crear ProductoRepository
        
        Returns:
            ProductoRepository: Instancia singleton del repositorio
        
        Raises:
            RuntimeError: Si BD no está inicializada
        
        Flujo FACTORY METHOD:
            1. if _database is None: raise error
            2. if _producto_repo is None: crear instancia
            3. return _producto_repo (singleton)
        
        Ejemplo:
            repo = RepositorioFactory.get_producto_repository()
            producto = repo.obtener("prod-001")
        """
        from infrastructure.repositories.database_store import DatabaseStore
        from infrastructure.repositories.producto_repository import ProductoRepository
        
        db = DatabaseStore.get_database()
        if cls._producto_repo is None:
            cls._producto_repo = ProductoRepository(db)
        return cls._producto_repo
