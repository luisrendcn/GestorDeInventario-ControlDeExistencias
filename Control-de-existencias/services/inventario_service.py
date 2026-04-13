"""
╔════════════════════════════════════════════════════════════════╗
║  ARCHIVO: services/inventario_service.py                       ║
║  FUNCIÓN: Servicios de movimientos de inventario              ║
╚════════════════════════════════════════════════════════════════╝

📋 RESPONSABILIDADES DEL ARCHIVO:
  • Implementar STRATEGY PATTERN con 3 estrategias de stock
  • Validar operaciones de stock
  • Registrar movimientos en historial
  • Persistir cambios de stock

🏭 PATRÓN: STRATEGY PATTERN
  • Define familia de 3 algoritmos intercambiables
  • Cada método = Una estrategia diferente
  • Cliente elige estrategia según contexto
  • Cada estrategia independiente y reutilizable

📊 ESTRATEGIAS IMPLEMENTADAS:

┌─────────────────────────────────────────────────────────────────────────────┐
│ Estrategia 1: ENTRADA_STOCK (entrada_stock)                                │
├─────────────────────────────────────────────────────────────────────────────┤
│ • Operación: SUMA de stock sin validar máximo                              │
│ • Contexto: Recepción de productos nuevos                                  │
│ • Validaciones: Solo cantidad positiva                                     │
│ • Limitaciones: Ninguna (puede crecer indefinidamente)                     │
│ • Ejemplo: Compra a proveedor, devoluciones                                │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ Estrategia 2: SALIDA_STOCK (salida_stock)                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│ • Operación: RESTA de stock CON validación                                 │
│ • Contexto: Venta/uso de productos existentes                              │
│ • Validaciones: Cantidad positiva + stock disponible                       │
│ • Limitaciones: NO puede exceder stock disponible                          │
│ • Ejemplo: Venta a cliente, retiro de almacén                              │
│                                                                             │
│ ⚠️ DIFERENCIA CLAVE: Esta estrategia verifica stock disponible              │
│    vs entrada_stock() que no lo valida                                     │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ Estrategia 3: AJUSTE_STOCK (ajuste_stock)                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│ • Operación: ASIGNA valor exacto sin suma/resta                            │
│ • Contexto: Corrección de inventario por auditoría                         │
│ • Validaciones: Stock no negativo                                          │
│ • Limitaciones: Solo no negativo, sin máximo                               │
│ • Ejemplo: Auditoría física, corrección de errores, robo detectado         │
└─────────────────────────────────────────────────────────────────────────────┘

🔄 FLUJO DE USO:
   Cliente (API) → selecciona estrategia según contexto
          ↓
   InventarioService.entrada_stock()  OR
   InventarioService.salida_stock()   OR
   InventarioService.ajuste_stock()
          ↓
   Cada estrategia ejecuta su algoritmo específico
          ↓
   Persistencia (BD + historial)

✅ BENEFICIOS:
  • Intercambiabilidad: Cambiar estrategia sin modificar código de cliente
  • Reutilización: Cada estrategia es independiente
  • Testabilidad: Cada estrategia se prueba por separado
  • Extensibilidad: Agregar nueva estrategia sin modificar existentes

📝 CONTRASTE CON IF/ELSE:
  ❌ Sin patrón: if tipo == 'entrada': ... elif tipo == 'salida': ... (acoplado)
  ✅ Con patrón: strategy.ejecutar() (desacoplado, polimórfico)
"""

from typing import Dict, Any
from core.exceptions import StockInsuficiente, DatosInvalidos
from core.schemas import MovimientoSchema
from .base_service import Service


class InventarioService(Service):
    """
    Servicios de movimientos de inventario (STRATEGY PATTERN).
    
    Implementa 3 estrategias intercambiables para cambiar stock de productos.
    Cada estrategia representa un tipo de movimiento diferente con su propia
    lógica de validación y cálculo.
    
    RESPONSABILIDADES (3):
      1️⃣  Estrategia ENTRADA: Sumar stock sin validar límites (entrada_stock)
          ├─ Usado para: Compras, devoluciones de clientes
          ├─ Validaciones: cantidad > 0
          └─ Sin límite máximo
      
      2️⃣  Estrategia SALIDA: Restar stock con validación (salida_stock)
          ├─ Usado para: Ventas, consumo, retiros
          ├─ Validaciones: cantidad > 0 AND cantidad <= stock disponible
          └─ Falla si stock insuficiente
      
      3️⃣  Estrategia AJUSTE: Asignar valor exacto (ajuste_stock)
          ├─ Usado para: Auditorías, correcciones, robos detectados
          ├─ Validaciones: nuevo_stock >= 0
          └─ Reemplaza el valor anterior sin aritmética
    
    FLUJO COMÚN A TODAS:
      1. Validar input schema
      2. Obtener producto actual
      3. Guardar stock_anterior
      4. Aplicar operación (agregar, restar o establecer)
      5. Persistir product o actualizado
      6. Registrar movimiento en historial
      7. Retornar resultado
    
    HERENCIA:
      Extiende BaseService (proporciona repository + validación)
    
    EXCEPCIONES LANZADAS:
      • DatosInvalidos: Si cantidad/nuevo_stock inválido
      • StockInsuficiente: Si salida_stock requiere más de lo disponible
      • ProductoNoEncontrado: Si producto_id no existe (de BaseService)
    
    REGISTRO DE HISTORIAL:
      • Todos los movimientos se registran en tabla movimientos
      • Contiene: tipo (ENTRADA/SALIDA/AJUSTE), cantidad, stock_anterior, stock_nuevo
      • Usado por ReporteService para auditoría y análisis
    """
    
    def entrada_stock(
        self, 
        producto_id: str, 
        cantidad: int, 
        motivo: str = 'Entrada'
    ) -> Dict[str, Any]:
        """
        ESTRATEGIA 1: Entrada de stock (suma sin validar máximo).
        
        Recibe productos nuevos sin validar límites.
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
        producto = self.validar_producto_existe(producto_id)
        stock_anterior = producto.stock
        
        # Aplicar estrategia
        producto.agregar_stock(cantidad)
        
        # Persistir
        self.repository.actualizar(producto)
        self.repository.registrar_movimiento(
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
    
    def salida_stock(
        self, 
        producto_id: str, 
        cantidad: int, 
        motivo: str = 'Salida'
    ) -> Dict[str, Any]:
        """
        ESTRATEGIA 2: Salida de stock (resta CON validación de disponibilidad).
        
        Venta/uso de productos con validación de stock disponible.
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
        producto = self.validar_producto_existe(producto_id)
        
        # VALIDAR STOCK DISPONIBLE (diferencia clave con entrada)
        if cantidad > producto.stock:
            raise StockInsuficiente(
                f"Stock insuficiente: disponible {producto.stock}, "
                f"solicitado {cantidad}"
            )
        
        stock_anterior = producto.stock
        
        # Aplicar estrategia
        producto.reducir_stock(cantidad)
        
        # Persistir
        self.repository.actualizar(producto)
        self.repository.registrar_movimiento(
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
    
    def ajuste_stock(
        self, 
        producto_id: str, 
        nuevo_stock: int, 
        motivo: str = 'Ajuste'
    ) -> Dict[str, Any]:
        """
        ESTRATEGIA 3: Ajuste de stock (asigna valor exacto para auditoría).
        
        Corrige inventario por auditoría, robo, pérdida, etc.
        """
        # Validar
        if nuevo_stock < 0:
            raise DatosInvalidos("El stock no puede ser negativo")
        
        # Obtener producto
        producto = self.validar_producto_existe(producto_id)
        stock_anterior = producto.stock
        
        # Aplicar estrategia
        producto.establecer_stock(nuevo_stock)
        cantidad = nuevo_stock - stock_anterior
        
        # Persistir
        self.repository.actualizar(producto)
        self.repository.registrar_movimiento(
            producto_id, 'AJUSTE', abs(cantidad),
            stock_anterior, producto.stock, motivo or 'Ajuste'
        )
        
        return {
            'producto_id': producto_id,
            'tipo': 'AJUSTE',
            'cantidad': cantidad,
            'stock_anterior': stock_anterior,
            'stock_nuevo': producto.stock,
            'motivo': motivo or 'Ajuste'
        }
