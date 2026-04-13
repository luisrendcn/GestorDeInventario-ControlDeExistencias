"""
╔════════════════════════════════════════════════════════════════════════════╗
║           ARCHIVO: services/inventario_strategies.py                      ║
║           FUNCIÓN: Estrategias de movimiento con SRP perfecto            ║
╚════════════════════════════════════════════════════════════════════════════╝

📋 RESPONSABILIDAD DEL ARCHIVO (3 CLASES - STRATEGY PATTERN):
   Cada clase implementa UNA estrategia de movimiento (SRP perfecto)

═════════════════════════════════════════════════════════════════════════════

📦 ESTRATEGIAS:

┌─ class EntradaStrategy (RESPONSABILIDAD: 1)
│  └─ Responsabilidad: Sumar stock sin validación máxima
│
┌─ class SalidaStrategy (RESPONSABILIDAD: 1)
│  └─ Responsabilidad: Restar stock con validación
│
┌─ class AjusteStrategy (RESPONSABILIDAD: 1)
│  └─ Responsabilidad: Asignar valor exacto de stock

🎯 PATRÓN: STRATEGY PATTERN (3 algoritmos intercambiables)
"""

from core.schemas import MovimientoSchema
from core.exceptions import StockInsuficiente, DatosInvalidos
from infrastructure.repositories import ProductoRepository, MovimientoRepository
from services.base_service import Service, ProductoValidator


class EntradaStrategy(Service):
    """
    Estrategia de ENTRADA de stock (suma sin validación máxima).
    
    RESPONSABILIDAD (1):
      1️⃣  Sumar stock sin validar límites
    
    Caso de uso: Recepción de compras, devoluciones de clientes
    
    Validaciones:
      • cantidad > 0
      • producto existe
    
    Sin limitaciones de máximo
    """
    
    def __init__(self, producto_repo: ProductoRepository, movimiento_repo: MovimientoRepository):
        """Inyectar ambos repositorios."""
        super().__init__(producto_repo)
        self.movimiento_repo = movimiento_repo
    
    def ejecutar(self, producto_id: str, cantidad: int, motivo: str = 'Entrada'):
        """
        Ejecutar estrategia de ENTRADA.
        
        RESPONSABILIDAD ÚNICA: Sumar stock
        
        Args:
            producto_id: ID del producto
            cantidad: Cantidad a sumar
            motivo: Razón de entrada
        
        Returns:
            dict: Resultado del movimiento
        
        Raises:
            DatosInvalidos: Si cantidad <= 0
            ProductoNoEncontrado: Si producto no existe
        """
        # Validar
        if cantidad <= 0:
            raise DatosInvalidos("La cantidad debe ser positiva")
        
        schema = MovimientoSchema(
            producto_id=producto_id,
            cantidad=cantidad,
            motivo=motivo or 'Entrada'
        )
        schema.validar()
        
        # Obtener producto
        producto = ProductoValidator.validar_existe(self.repository, producto_id)
        stock_anterior = producto.stock
        
        # Aplicar estrategia: SUMA sin límite
        producto.agregar_stock(cantidad)
        
        # Persistir
        self.repository.actualizar(producto)
        self.movimiento_repo.registrar_movimiento(
            producto_id, 'ENTRADA', cantidad,
            stock_anterior, producto.stock, motivo or 'Entrada'
        )
        
        return {
            'producto_id': producto_id,
            'tipo': 'ENTRADA',
            'cantidad': cantidad,
            'stock_anterior': stock_anterior,
            'stock_nuevo': producto.stock,
            'motivo': motivo or 'Entrada'
        }


class SalidaStrategy(Service):
    """
    Estrategia de SALIDA de stock (resta con validación).
    
    RESPONSABILIDAD (1):
      1️⃣  Restar stock CON validación de disponibilidad
    
    Caso de uso: Ventas, retiros de almacén
    
    Validaciones:
      • cantidad > 0
      • cantidad <= stock disponible
      • producto existe
    
    DIFERENCIA CLAVE: Valida que hay suficiente stock (vs ENTRADA que no)
    """
    
    def __init__(self, producto_repo: ProductoRepository, movimiento_repo: MovimientoRepository):
        """Inyectar ambos repositorios."""
        super().__init__(producto_repo)
        self.movimiento_repo = movimiento_repo
    
    def ejecutar(self, producto_id: str, cantidad: int, motivo: str = 'Salida'):
        """
        Ejecutar estrategia de SALIDA.
        
        RESPONSABILIDAD ÚNICA: Restar stock con validación
        
        Args:
            producto_id: ID del producto
            cantidad: Cantidad a restar
            motivo: Razón de salida
        
        Returns:
            dict: Resultado del movimiento
        
        Raises:
            DatosInvalidos: Si cantidad <= 0
            StockInsuficiente: Si cantidad > stock disponible
            ProductoNoEncontrado: Si producto no existe
        """
        # Validar
        if cantidad <= 0:
            raise DatosInvalidos("La cantidad debe ser positiva")
        
        schema = MovimientoSchema(
            producto_id=producto_id,
            cantidad=cantidad,
            motivo=motivo or 'Salida'
        )
        schema.validar()
        
        # Obtener producto
        producto = ProductoValidator.validar_existe(self.repository, producto_id)
        
        # VALIDAR DISPONIBILIDAD (DIFERENCIA CLAVE CON ENTRADA)
        if cantidad > producto.stock:
            raise StockInsuficiente(
                f"Stock insuficiente: disponible {producto.stock}, "
                f"solicitado {cantidad}"
            )
        
        stock_anterior = producto.stock
        
        # Aplicar estrategia: RESTA con validación
        producto.reducir_stock(cantidad)
        
        # Persistir
        self.repository.actualizar(producto)
        self.movimiento_repo.registrar_movimiento(
            producto_id, 'SALIDA', cantidad,
            stock_anterior, producto.stock, motivo or 'Salida'
        )
        
        return {
            'producto_id': producto_id,
            'tipo': 'SALIDA',
            'cantidad': cantidad,
            'stock_anterior': stock_anterior,
            'stock_nuevo': producto.stock,
            'motivo': motivo or 'Salida'
        }


class AjusteStrategy(Service):
    """
    Estrategia de AJUSTE de stock (asigna valor exacto).
    
    RESPONSABILIDAD (1):
      1️⃣  Asignar valor exacto sin aritmética
    
    Caso de uso: Auditoría física, correcciones por robo/pérdida
    
    Validaciones:
      • nuevo_stock >= 0
      • producto existe
    
    SIN aritmética, solo asignación directa
    """
    
    def __init__(self, producto_repo: ProductoRepository, movimiento_repo: MovimientoRepository):
        """Inyectar ambos repositorios."""
        super().__init__(producto_repo)
        self.movimiento_repo = movimiento_repo
    
    def ejecutar(self, producto_id: str, nuevo_stock: int, motivo: str = 'Ajuste'):
        """
        Ejecutar estrategia de AJUSTE.
        
        RESPONSABILIDAD ÚNICA: Asignar valor exacto
        
        Args:
            producto_id: ID del producto
            nuevo_stock: Nuevo valor de stock (asignación directa)
            motivo: Razón del ajuste
        
        Returns:
            dict: Resultado del movimiento
        
        Raises:
            DatosInvalidos: Si nuevo_stock < 0
            ProductoNoEncontrado: Si producto no existe
        """
        # Validar
        if nuevo_stock < 0:
            raise DatosInvalidos("El stock no puede ser negativo")
        
        # Obtener producto
        producto = ProductoValidator.validar_existe(self.repository, producto_id)
        stock_anterior = producto.stock
        
        # Calcular cantidad para el historial
        cantidad = nuevo_stock - stock_anterior
        
        # Aplicar estrategia: ASIGNACIÓN directa sin aritmética
        producto.establecer_stock(nuevo_stock)
        
        # Persistir
        self.repository.actualizar(producto)
        self.movimiento_repo.registrar_movimiento(
            producto_id, 'AJUSTE', abs(cantidad),
            stock_anterior, producto.stock, motivo or 'Ajuste'
        )
        
        return {
            'producto_id': producto_id,
            'tipo': 'AJUSTE',
            'stock_anterior': stock_anterior,
            'stock_nuevo': nuevo_stock,
            'diferencia': cantidad,
            'motivo': motivo or 'Ajuste'
        }
