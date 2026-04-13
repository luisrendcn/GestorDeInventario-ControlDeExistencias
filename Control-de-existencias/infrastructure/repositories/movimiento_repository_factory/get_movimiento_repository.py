"""
╔════════════════════════════════════════════════════════════════════════════╗
║   ARCHIVO: movimiento_repository_factory/get_movimiento_repository.py     ║
║   RESPONSABILIDAD: Factory para crear MovimientoRepository                ║
╚════════════════════════════════════════════════════════════════════════════╝

🎯 ÚNICA RESPONSABILIDAD:
   Factory que crea instancia singleton de MovimientoRepository.
"""


class GetMovimientoRepositoryMixin:
    """
    Mixin que agrega factory method para MovimientoRepository.
    
    RESPONSABILIDAD: 1
    • Crear instancia singleton de MovimientoRepository
    
    Requiere:
        • _movimiento_repo (class variable)
        • DatabaseStore.get_database()
        • MovimientoRepository (importar)
    """
    
    @classmethod
    def get_movimiento_repository(cls):
        """
        🏭 Obtener repositorio de movimientos (FACTORY METHOD).
        
        Factory que implementa:
          • Validación de precondiciones
          • Instanciación perezosa (lazy initialization)
          • Singleton Pattern (una única instancia)
        
        RESPONSABILIDAD: Crear MovimientoRepository
        
        Returns:
            MovimientoRepository: Instancia singleton del repositorio
        
        Raises:
            RuntimeError: Si BD no está inicializada
        
        Flujo FACTORY METHOD:
            1. if _database is None: raise error
            2. if _movimiento_repo is None: crear instancia
            3. return _movimiento_repo (singleton)
        
        Ejemplo:
            repo = MovimientoRepositoryFactory.get_movimiento_repository()
            movs = repo.obtener_historial()
        """
        from infrastructure.repositories.database_store import DatabaseStore
        from infrastructure.repositories.movimiento_repository import MovimientoRepository
        
        db = DatabaseStore.get_database()
        if cls._movimiento_repo is None:
            cls._movimiento_repo = MovimientoRepository(db)
        return cls._movimiento_repo
