╔═══════════════════════════════════════════════════════════════════════════╗
║             GUÍA RÁPIDA: PATRONES DE DISEÑO - ARCHIVOS A MOSTRAR         ║
║                  (Para usar durante grabación del video)                  ║
╚═══════════════════════════════════════════════════════════════════════════╝

DURACIÓN TOTAL DEL VIDEO: ~15-17 minutos
FORMATO: Narrativo + Demostración de código en VS Code

═════════════════════════════════════════════════════════════════════════════════

1️⃣  PATRÓN: FACADE (Fachada ~ 3-4 minutos)
───────────────────────────────────────────────────────────────────────────────

PROBLEMA QUE RESUELVE:
  → Ocultar complejidad de múltiples subsistemas detrás de una interfaz simple

CÓMO ESTÁ IMPLEMENTADO:
  → FlaskApplication orquesta: BD, middlewares, rutas, blueprints
  → DatabaseManager orquesta: conexión, schema, productos, historial, reportes

ARCHIVOS A MOSTRAR:
  
  📄 FACADE #1: FlaskApplication
     Archivo: app/application.py
     Líneas a mostrar:
       • Líneas 1-30: Docstring y imports
       • Líneas 26-76: Clase completa con initialize()
       • Mostrar especialmente líneas 49-76 donde orquesta

     QUÉ OBSERVAR:
       - Línea 52-53: inicializa BD
       - Línea 56-57: registra middlewares
       - Línea 60-61: registra rutas
       - Línea 64-65: registra blueprints
       Cada paso delega a una clase especializada ✓

  📄 FACADE #2: DatabaseManager
     Archivo: database/__init__.py
     Líneas a mostrar:
       • Líneas 1-50: Docstring del FACADE
       • Líneas 55-80: Clase y método conectar()
       • Líneas 100-180: Métodos que delegan a componentes

     QUÉ OBSERVAR:
       - Cómo delega a 6 componentes (connection, schema, productos, etc)
       - Interfaz simple: .conectar(), .crear_producto(), .obtener_reporte()
       - Cliente no ve complejidad interna ✓

═════════════════════════════════════════════════════════════════════════════════

2️⃣  PATRÓN: FACTORY METHOD (Fábrica ~ 3-4 minutos)
───────────────────────────────────────────────────────────────────────────────

PROBLEMA QUE RESUELVE:
  → Centralizar la creación compleja de objetos en UN ÚNICO LUGAR
  → Evitar duplicación de lógica de creación

CÓMO ESTÁ IMPLEMENTADO:
  → create_app() centraliza creación de la aplicación Flask
  → RepositorioFactory centraliza creación de repositorios (Singleton)
  → MovimientoRepositoryFactory centraliza creación de repositorio de movimientos

ARCHIVOS A MOSTRAR:

  📄 FACTORY METHOD #1: create_app()
     Archivo: app/__init__.py
     Líneas a mostrar:
       • Líneas 14-30: Función create_app()
       • Línea 33: Instancia global app = create_app()

     QUÉ OBSERVAR:
       - Línea 14-26: Función factory que crea y retorna app
       - Responsabilidad única: crear la app correctamente
       - Cliente hace: from app import app ← ¡Simple!
       - O: app = create_app() ← ¡Reutilizable!

  📄 FACTORY METHOD #2: RepositorioFactory
     Archivo: infrastructure/repositories/repositorio_factory/__init__.py
     Líneas a mostrar:
       • Líneas 1-30: Clase completa

     QUÉ OBSERVAR:
       - _producto_repo = None (línea 23)
       - @classmethod get_producto_repository(cls) - Factory method
       - if cls._producto_repo is None → Singleton pattern
       - Una única instancia compartida ✓

  📄 FACTORY METHOD #3: MovimientoRepositoryFactory
     Archivo: infrastructure/repositories/movimiento_repository_factory/__init__.py
     Líneas a mostrar:
       • Líneas 1-30: Patrón idéntico a RepositorioFactory

     QUÉ OBSERVAR:
       - Mismo patrón que RepositorioFactory
       - Centralización de creación ✓

═════════════════════════════════════════════════════════════════════════════════

3️⃣  PATRÓN: STRATEGY (Estrategias ~ 4-5 minutos)
───────────────────────────────────────────────────────────────────────────────

PROBLEMA QUE RESUELVE:
  → Múltiples algoritmos intercambiables sin usar if/else
  → Cada algoritmo es independiente y testeable

CÓMO ESTÁ IMPLEMENTADO:
  → 3 estrategias de movimiento de stock:
    1. EntradaStrategy: suma stock SIN validación
    2. SalidaStrategy: resta stock CON validación > 0
    3. AjusteStrategy: asigna valor exacto
  → Todas implementan interfaz execute()

ARCHIVOS A MOSTRAR:

  📄 STRATEGY: Definición de estrategias
     Archivo: services/inventario_strategies.py
     Líneas a mostrar:
       • Líneas 1-100: Documentación + explicación del patrón
       • Línea 40-60: explicación detallada
       • Línea 70-110: Contraste if/else vs STRATEGY

     QUÉ OBSERVAR:
       - Patrón BIEN DOCUMENTADO
       - Problema de if/else explicado
       - Solución con clases independientes

  📄 STRATEGY: EntradaStrategy
     Archivo: services/inventario_strategies.py
     Líneas a mostrar:
       • Líneas 115-170: Clase EntradaStrategy

     QUÉ OBSERVAR:
       - Hereda de BaseStrategy
       - Método execute() suma stock SIN validación
       - Lógica independiente ✓

  📄 STRATEGY: SalidaStrategy
     Archivo: services/inventario_strategies.py
     Líneas a mostrar:
       • Líneas 175-230: Clase SalidaStrategy

     QUÉ OBSERVAR:
       - Hereda de BaseStrategy
       - Método execute() VALIDA stock >= cantidad
       - Diferente lógica que Entrada
       - Ambas comparten interfaz execute() ✓

  📄 STRATEGY: AjusteStrategy
     Archivo: services/inventario_strategies.py
     Líneas a mostrar:
       • Líneas 235-280: Clase AjusteStrategy

     QUÉ OBSERVAR:
       - Hereda de BaseStrategy
       - Método execute() asigna valor exacto
       - Ninguna validación
       - Tercera opción diferente ✓

  📄 STRATEGY: USO EN API
     Archivo: api/v1/movimientos.py
     Líneas a mostrar:
       • Líneas 80-120: Función entrada()
       • Líneas 150-190: Función salida()
       • Líneas 220-260: Función ajuste()

     QUÉ OBSERVAR:
       - En CADA endpoint:
         strategy = ServiceContainer.get_X_strategy()
         resultado = strategy.ejecutar(...)
       - Cliente NO conoce detalles de cada estrategia
       - Solo elige y ejecuta ✓

═════════════════════════════════════════════════════════════════════════════════

4️⃣  PATRÓN: OBSERVER (Observadores ~ 4-5 minutos)
───────────────────────────────────────────────────────────────────────────────

PROBLEMA QUE RESUELVE:
  → Notificaciones automáticas sin acoplar código
  → Múltiples sistemas reaccionan a eventos sin conocerse entre sí

CÓMO ESTÁ IMPLEMENTADO:
  → EventManager: coordinador central
  → Events: tipos de eventos que pueden ocurrir
  → Observers: listeners que reaccionan a eventos
  → Listeners concretos: AlertasListener, AuditoriaListener, NotificacionesListener

ARCHIVOS A MOSTRAR:

  📄 OBSERVER: Event (clases de eventos)
     Archivo: core/event_system/event.py
     Líneas a mostrar:
       • Líneas 1-30: Docstring
       • Líneas 10-30: Clase Event base
       • Líneas 35-65: StockBajoEvent, ProductoAgotadoEvent, etc

     QUÉ OBSERVAR:
       - Cada evento encapsula información
       - Event base con timestamp
       - StockBajoEvent contiene: producto_id, stock, stock_minimo ✓

  📄 OBSERVER: Observer Interface
     Archivo: core/event_system/observer.py
     Líneas a mostrar:
       • Líneas 1-15: Interfaz Observer completa

     QUÉ OBSERVAR:
       - Clase abstracta con método update()
       - Contrato que todos los listeners deben cumplir
       - Simple pero poderoso ✓

  📄 OBSERVER: EventManager
     Archivo: core/event_system/event_manager.py
     Líneas a mostrar:
       • Líneas 1-50: Clase EventManager
       • Línea 20-35: Método subscribe()
       • Línea 37-45: Método unsubscribe()
       • Línea 47-65: Método emit()

     QUÉ OBSERVAR:
       - Línea 19: _observers dict guarda listeners por tipo
       - subscribe(): registra listener para evento
       - unsubscribe(): desregistra listener
       - emit(): dispara a TODOS los listeners suscritos ✓

  📄 OBSERVER: Listeners Concretos
     Archivo: core/event_system/listeners.py
     Líneas a mostrar:
       • Líneas 1-35: Clase AlertasListener
       • Líneas 40-65: Clase AuditoriaListener
       • Líneas 70-150: Clase NotificacionesListener

     QUÉ OBSERVAR:
       - Cada listener implementa update(event)
       - AlertasListener: genera alertas visuales ⚠️
       - AuditoriaListener: registra en log 📝
       - NotificacionesListener: crea notificaciones 📧
       - Cada uno maneja SU responsabilidad
       - Sin acoplamiento entre ellos ✓

═════════════════════════════════════════════════════════════════════════════════

📋 TABLA RESUMEN PARA REFERENCIAS RÁPIDAS
───────────────────────────────────────────────────────────────────────────────

PATRÓN          | ARCHIVO PRINCIPAL           | LÍNEAS CLAVE
─────────────────────────────────────────────────────────────────────────────
FACADE          | app/application.py          | 26-76 (clase + initialize)
                | database/__init__.py        | 55-80 + 100-180
─────────────────────────────────────────────────────────────────────────────
FACTORY METHOD  | app/__init__.py             | 14-30 (función create_app)
                | repositorio_factory/__init__| 1-30
                | movimiento_repo_factory/... | 1-30
─────────────────────────────────────────────────────────────────────────────
STRATEGY        | inventario_strategies.py    | 1-100 (docs)
                |                             | 115-280 (3 strategies)
                | api/v1/movimientos.py       | 80-120 (uso)
─────────────────────────────────────────────────────────────────────────────
OBSERVER        | event.py                    | 1-70 (Events)
                | observer.py                 | 1-15 (Interface)
                | event_manager.py            | 1-80 (Manager)
                | listeners.py                | 1-150 (Listeners)
─────────────────────────────────────────────────────────────────────────────

═════════════════════════════════════════════════════════════════════════════════

🎬 INSTRUCCIONES PARA GRABAR:
───────────────────────────────────────────────────────────────────────────────

PASO 1: PREPARACIÓN
  ✓ Abre VS Code
  ✓ Abre la carpeta Control-de-existencias
  ✓ Aumento el font size a 16-18pt (Settings > Font Size)
  ✓ Usa tema oscuro (cmd/ctrl + K, cmd/ctrl + T → busca tema oscuro)
  ✓ Desactiva minimap (View > Toggle Minimap)
  ✓ Ten a mano este documento para referencias

PASO 2: DURANTE LA GRABACIÓN
  ✓ Lee narración del GUION_VIDEO_PATRONES.md
  ✓ Abre archivos EN EL ORDEN listado arriba
  ✓ Scroll lentamente (viewers necesitan leer código)
  ✓ Usa Ctrl+G para ir a línena específica (Go to line)
  ✓ Resalta con hover las líneas importantes
  ✓ Pausa entre patrones (2-3 segundos)

PASO 3: EDICIÓN (después de grabar)
  ✓ Agrega intro de 10 segundos
  ✓ Agrega índice visual de patrones
  ✓ Agrega transiciones entre cada patrón
  ✓ Agrega sonido de fondo subtle
  ✓ Agrega captions/subtítulos
  ✓ Duración final: 15-17 minutos

═════════════════════════════════════════════════════════════════════════════════
