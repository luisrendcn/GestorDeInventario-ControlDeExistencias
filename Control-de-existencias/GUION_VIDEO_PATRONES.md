╔═══════════════════════════════════════════════════════════════════════════╗
║                GUION VIDEO: PATRONES DE DISEÑO - VERSIÓN CONCISA         ║
║                    "4 patrones en ~7-8 minutos"                         ║
╚═══════════════════════════════════════════════════════════════════════════╝

👋 INTRO (15 segundos)
───────────────────────────────────────────────────────────────────────────────

"Este video muestra 4 patrones de diseño implementados en un sistema real de 
gestión de inventario. Veremos cómo cada patrón resuelve un problema específico 
en el código."

═════════════════════════════════════════════════════════════════════════════════
#1: FACADE - Simplificar complejidad (~1.5 minutos)
═════════════════════════════════════════════════════════════════════════════════

"PROBLEMA: Múltiples subsistemas complejos (BD, middlewares, rutas, errores).

SOLUCIÓN FACADE: Una interfaz simple que oculta la complejidad."

[ABRIR: app/application.py - Líneas 26-76]

"FlaskApplication ORQUESTA todo:
  • Línea 52-53: Inicializa BD
  • Línea 56-57: Registra middlewares
  • Línea 60-61: Registra rutas
  • Línea 64-65: Registra blueprints

El cliente solo llama: app = create_app() ✓

[ABRIR: database/__init__.py - Líneas 55-80]

DatabaseManager es otro FACADE que oculta 6 componentes:
  • Connection, SchemaCreator, ProductOperations, etc.

Cliente usa: db.crear_producto() sin saber los detalles internos. ✓"

═════════════════════════════════════════════════════════════════════════════════
#2: FACTORY METHOD - Centralizar creación (~1 minuto)
═════════════════════════════════════════════════════════════════════════════════

"PROBLEMA: Crear objetos complejos en múltiples lugares = duplicación.

SOLUCIÓN FACTORY: Una función/clase que centraliza la construcción."

[ABRIR: app/__init__.py - Líneas 14-30]

"create_app() es el factory que crea la aplicación Flask.
  • Lógica centralizada
  • Cambios en un lugar
  • Reutilizable en tests

[ABRIR: infrastructure/repositories/repositorio_factory/__init__.py]

RepositorioFactory también usa Factory + Singleton:
  • Una única instancia de ProductoRepository
  • Eficiente (evita múltiples conexiones BD) ✓"

═════════════════════════════════════════════════════════════════════════════════
#3: STRATEGY - Algoritmos intercambiables (~2 minutos)
═════════════════════════════════════════════════════════════════════════════════

"PROBLEMA: ¿Cómo cambiar stock? Múltiples formas sin usar if/else complejo.

SOLUCIÓN STRATEGY: Cada algoritmo en su propia clase."

[ABRIR: services/inventario_strategies/]

"3 estrategias en carpetas separadas:

[MOSTRAR entrada/]
EntradaStrategy: suma stock (sin validación)
  • entrada_strategy.py (orquestador)
  • validar_entrada.py (validación)
  • sumar_stock.py (operación)
  • registrar_entrada.py (persistencia)

[MOSTRAR salida/]
SalidaStrategy: resta stock (CON validación - DIFERENCIA CLAVE)
  • validar_salida.py incluye: validar_disponibilidad()

[MOSTRAR ajuste/]
AjusteStrategy: asigna valor exacto

[ABRIR: api/v1/movimientos.py - Líneas 80-120]

Cliente usa:
  strategy = ServiceContainer.get_salida_strategy()
  resultado = strategy.ejecutar(...)

Transparente. La arquitectura interna no afecta al cliente. ✓"

═════════════════════════════════════════════════════════════════════════════════
#4: OBSERVER - Notificaciones automáticas (~2 minutos)
═════════════════════════════════════════════════════════════════════════════════

"PROBLEMA: Cuando algo importante ocurre (stock bajo), muchos sistemas necesitan 
saberlo. ¿Cómo evitar acoplamiento?

SOLUCIÓN OBSERVER: Publisher emite eventos. Observers escuchan sin conocerse."

[ABRIR: core/event_system/event.py - Líneas 1-70]

"Definimos eventos:
  • Event (clase base)
  • StockBajoEvent
  • ProductoAgotadoEvent
  • MovimientoRegistradoEvent

[ABRIR: core/event_system/observer.py]

Observer es la interfaz que todos deben cumplir:
  def update(self, event: Event) -> None

[ABRIR: core/event_system/event_manager.py - Líneas 1-60]

EventManager COORDINA:
  • subscribe(): Los observers se registran
  • emit(): El publisher dispara eventos
  • Listeners reaccionan automáticamente

[ABRIR: core/event_system/listeners.py - Líneas 1-150]

3 listeners concretos:
  • AlertasListener: genera alertas ⚠️
  • AuditoriaListener: registra eventos 📝
  • NotificacionesListener: crea notificaciones 📧

FLUJO: stock cae → event_manager.emit(StockBajoEvent) → 
todos los listeners reaccionan automáticamente. ✓"

═════════════════════════════════════════════════════════════════════════════════
🎯 CONCLUSIÓN (20 segundos)
═════════════════════════════════════════════════════════════════════════════════

"4 patrones, 1 sistema:
  • FACADE → Simplifica complejidad
  • FACTORY → Centraliza creación
  • STRATEGY → Algoritmos intercambiables
  • OBSERVER → Reactividad desacoplada

Hacen el código mantenible, testeable y escalable.

Gracias por ver! 👋"

═════════════════════════════════════════════════════════════════════════════════

📋 ARCHIVOS A TENER ABIERTOS (en orden):

1. app/application.py (líneas 26-76) - FACADE #1
2. database/__init__.py (líneas 55-80) - FACADE #2
3. app/__init__.py (líneas 14-30) - FACTORY #1
4. infrastructure/repositories/repositorio_factory/__init__.py - FACTORY #2
5. services/inventario_strategies/entrada/entrada_strategy.py - STRATEGY
6. services/inventario_strategies/salida/salida_strategy.py - STRATEGY
7. services/inventario_strategies/ajuste/ajuste_strategy.py - STRATEGY
8. api/v1/movimientos.py (líneas 80-120) - USO STRATEGY
9. core/event_system/event.py - OBSERVER
10. core/event_system/observer.py - OBSERVER
11. core/event_system/event_manager.py - OBSERVER
12. core/event_system/listeners.py - OBSERVER

⏱️  TIMING: ~7-8 minutos total
🎨 TIP: Font 16-18pt, tema oscuro, pausas entre patrones
