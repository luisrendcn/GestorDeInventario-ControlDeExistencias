╔═══════════════════════════════════════════════════════════════════════════╗
║                    GUION VIDEO: PATRONES DE DISEÑO                        ║
║         "Patrones aplicados en el sistema de inventario"                 ║
║                          (~15 minutos)                                    ║
╚═══════════════════════════════════════════════════════════════════════════╝

───────────────────────────────────────────────────────────────────────────────

👋 INTRO (30 segundos)
───────────────────────────────────────────────────────────────────────────────

"Hola, en este video te voy a mostrar cómo en este sistema de gestión de 
inventario hemos aplicado cuatro patrones de diseño fundamentales del mundo 
profesional. Verás cómo cada patrón resuelve un problema específico y cómo 
están implementados en el código real del proyecto."

[TRANSICIÓN: Mostrar pantalla del escritorio con VS Code]

───────────────────────────────────────────────────────────────────────────────

📊 ÍNDICE (20 segundos)
───────────────────────────────────────────────────────────────────────────────

"Vamos a cubrir 4 patrones de diseño hoy:

  1️⃣  FACADE - La cara visible de un sistema complejo
  2️⃣  FACTORY METHOD - La fábrica centralizada
  3️⃣  STRATEGY - Intercambiabilidad de algoritmos
  4️⃣  OBSERVER - Notificaciones automáticas

Empecemos..."

[TRANSICIÓN: Fade to black, esperar 2 segundos]

═════════════════════════════════════════════════════════════════════════════════
PATRÓN #1: FACADE (FACHADA)
═════════════════════════════════════════════════════════════════════════════════

📖 EXPLICACIÓN (1 minuto 30 segundos)
───────────────────────────────────────────────────────────────────────────────

"El PRIMERO es el patrón FACADE.

[ESCRIBIR EN PIZARRA MENTAL O CON GRÁFICO]

¿CUÁL ES EL PROBLEMA?

Imagina que tienes un sistema complejo con muchos subsistemas:
- Base de datos
- Middlewares
- Rutas y endpoints
- Manejo de errores
- Autenticación

Todo interconectado y difícil de coordinar. El cliente que quiere usar tu 
aplicación NO quiere saber de todos estos detalles internos. Solo quiere:

  'Iniciá la app, listo.'

SOLUCIÓN - PATRÓN FACADE:

Creas UNA interfaz simplificada que OCULTA toda la complejidad interna y:
- Coordina todos los subsistemas tras bastidores
- Presenta una interfaz simple al cliente
- Mantiene consistencia en la inicialización

En nuestro caso, la aplicación Flask necesita:
  1. Conectar a la BD
  2. Crear tablas
  3. Registrar middlewares (logging, manejo de errores)
  4. Registrar rutas
  5. Registrar blueprints de API

TODO ESTO está coordinado por UN ÚNICOLUGAR: La clase FlaskApplication.

[ABRIR VS CODE - PREPARAR PARA MOSTRAR CÓDIGO]"

───────────────────────────────────────────────────────────────────────────────

💻 CÓDIGO - FACADE #1: FlaskApplication (2 minutos)
───────────────────────────────────────────────────────────────────────────────

[ABRIR ARCHIVO y MOSTRAR]

Archivo: app/application.py
Líneas: 1-50 (comentarios + descripción)

"Aquí está. Ves la clase FlaskApplication. Esta es nuestra FACHADA.

[MOSTRAR LÍNEAS 26-75 - La clase y su método initialize()]

En el método 'initialize()' (línea 49-76), ves exactamente lo que dije:

PASO 1 (línea 52-53): Inicializar BD
PASO 2 (línea 56-57): Registrar middlewares
PASO 3 (línea 60-61): Registrar rutas
PASO 4 (línea 64-65): Registrar blueprints

Si ves, cada paso delega a una clase especializada:
- DatabaseInitializer
- MiddlewareRegistry
- RoutesRegistry
- BlueprintRegistry

Pero el CLIENTE (quien crea la app) nunca se entera de esto. Solo escribe:

  app = create_app()  ← ¡Listo! Todo inicializado.

Eso es el FACADE: Una interfaz simple que oculta complejidad."

───────────────────────────────────────────────────────────────────────────────

💻 CÓDIGO - FACADE #2: DatabaseManager (1 minuto)
───────────────────────────────────────────────────────────────────────────────

"Tenemos un SEGUNDO Facade en la capa de base de datos.

[ABRIR ARCHIVO]

Archivo: database/__init__.py
Líneas: 1-80 (definición de clase DatabaseManager)

Aquí, DatabaseManager es otra FACHADA que oculta:
- DatabaseConnection
- SchemaCreator
- ProductOperations
- HistoryManager
- ReportGenerator
- DemoManager

Todo coordinado en UN LUGAR. 

Mira las líneas [100-180], cómo delega cada método a un componente específico.
El usuario de la BD no necesita saber de 6 componentes. Solo llama:

  db.conectar()
  db.crear_producto(...)
  db.obtener_reporte()

SIMPLE. Eso es FACADE."

───────────────────────────────────────────────────────────────────────────────

✅ RESUMEN - FACADE
───────────────────────────────────────────────────────────────────────────────

"FACADE PATTERN RESUELVE:

  ✓ Complejidad: Múltiples componentes → UNA interfaz simple
  ✓ Mantenibilidad: Cambios internos no afectan al cliente
  ✓ Escalabilidad: Agregar nuevos subsistemas sin romper API

EN NUESTRO PROYECTO:
  • FlaskApplication → Orquesta toda la inicialización de Flask
  • DatabaseManager → Orquesta toda la capa de persistencia

[TRANSICIÓN: Pausa 1 segundo]"

═════════════════════════════════════════════════════════════════════════════════
PATRÓN #2: FACTORY METHOD
═════════════════════════════════════════════════════════════════════════════════

📖 EXPLICACIÓN (1 minuto 30 segundos)
───────────────────────────────────────────────────────────────────────────────

"SEGUNDO patrón: FACTORY METHOD - La Fábrica.

¿CUÁL ES EL PROBLEMA?

Cuando necesitas CREAR objetos complejos, tres problemas pasan:

1. El código de creación es LARGO y REPETITIVO
2. Si cambia la LÓGICA DE CREACIÓN, hay que actualizar MUCHOS LUGARES
3. El cliente no debería saber CÓMO se crea el objeto

Ejemplo: Crear una aplicación Flask requiere:
- Instanciar Flask()
- Cargar configuración
- Inicializar BD
- Registrar middlewares
- Registrar blueprints

Si haces esto en CADA LUGAR donde necesitas la app, repites código. ¡Error!

SOLUCIÓN - FACTORY METHOD:

Creas UNA FUNCIÓN O MÉTODO que CENTRALIZA la creación:

  def create_app():
      app = FlaskApplication()
      return app.initialize()

Luego, SIEMPRE que necesites la app:

  app = create_app()

¿CAMBIÓ la lógica de creación? Actualizas UN LUGAR. Listo.

EN NUESTRO PROYECTO:"

───────────────────────────────────────────────────────────────────────────────

💻 CÓDIGO - FACTORY METHOD #1: create_app() (1 minuto 30 segundos)
───────────────────────────────────────────────────────────────────────────────

"[ABRIR ARCHIVO]

Archivo: app/__init__.py
Líneas: 14-30 (función create_app)

Aquí está el factory.

[MOSTRAR FUNCIÓN]

La función 'create_app()' (línea 14-30) centraliza cómo se crea la aplicación Flask.

¿Necesitas la app en run.py? 

  from app import app

¿Necesitas la app en tests? 

  from app import create_app
  app = create_app()

Una ÚNICA FUENTE DE VERDAD. Si la lógica de creación cambia, actualizas aquí y 
toda la aplicación lo refleja inmediatamente.

Nota que esta función LLAMA a FlaskApplication (que es un FACADE).
Así combinamos FACTORY + FACADE.

FACTORY encapsula ¿CÓMO? se crea.
FACADE encapsula ¿QUÉ? necesita hacer."

───────────────────────────────────────────────────────────────────────────────

💻 CÓDIGO - FACTORY METHOD #2: Repositories (1 minuto)
───────────────────────────────────────────────────────────────────────────────

"Hay OTRO factory en los repositorios.

[ABRIR ARCHIVO]

Archivo: infrastructure/repositories/repositorio_factory/__init__.py
Líneas: 1-30

La clase 'RepositorioFactory' es un factory que crea ProductoRepository.

[MOSTRAR CÓDIGO]

Ves que:
  • _producto_repo = None  (comienza sin instancia)
  • get_producto_repository()  (crear si no existe)
  • Usa Singleton Pattern (una única instancia)

¿POR QUÉ?

Porque crear un repositorio es costoso (conecta a BD, configura queries).
Si lo hacemos en 50 lugares diferentes, 50 conexiones abiertas.

Con FACTORY:

  repo = RepositorioFactory.get_produto_repository()

Siempre la MISMA instancia. Eficiente.

Lo mismo ocurre con MovimientoRepositoryFactory.

[MOSTRAR]

Archivo: infrastructure/repositories/movimiento_repository_factory/__init__.py
Líneas: 1-30"

───────────────────────────────────────────────────────────────────────────────

✅ RESUMEN - FACTORY METHOD
───────────────────────────────────────────────────────────────────────────────

"FACTORY METHOD RESUELVE:

  ✓ Centralización: Lógica de creación en UN LUGAR
  ✓ Reutilización: Evita duplicación de código
  ✓ Cambios: Modificar la creación sin tocar el cliente
  ✓ Singleton: Una única instancia compartida (cuando aplica)

EN NUESTRO PROYECTO:
  • create_app() → Factory de la aplicación Flask
  • RepositorioFactory → Factory de ProductoRepository
  • MovimientoRepositoryFactory → Factory de MovimientoRepository

[TRANSICIÓN]"

═════════════════════════════════════════════════════════════════════════════════
PATRÓN #3: STRATEGY
═════════════════════════════════════════════════════════════════════════════════

📖 EXPLICACIÓN (1 minuto 30 segundos)
───────────────────────────────────────────────────────────────────────────────

"TERCERO: STRATEGY PATTERN - Las Estrategias.

¿CUÁL ES EL PROBLEMA?

Tienes un proceso COMPLEJO con MÚLTIPLES ALTERNATIVAS.

En un sistema de inventario, ¿cómo cambias el stock?

OPCIÓN 1 (MALA - Con if/else):

  function cambiar_stock(producto_id, operacion, cantidad):
      if operacion == 'entrada':
          // suma stock SIN validación
      else if operacion == 'salida':
          // resta stock CON validación > 0
      else if operacion == 'ajuste':
          // asigna valor exacto

Problemas:
  ✗ Lógica compleja y difícil de leer
  ✗ Si agreguás nueva estrategia, modificas el if/else (violás OPEN/CLOSED)
  ✗ Difícil de testear cada estrategia
  ✗ Mezcla de conceptos en una función

SOLUCIÓN - STRATEGY PATTERN:

Extraes CADA alternativa en su PROPIA CLASE:

  • EntradaStrategy: suma stock SIN validación
  • SalidaStrategy: resta stock CON validación
  • AjusteStrategy: asigna valor exacto

Luego el cliente ELIGE QUÉ ESTRATEGIA usar:

  strategy = ServiceContainer.get_entrada_strategy()
  resultado = strategy.ejecutar(...)

¿Querés agregar una nueva estrategia? Creas nueva clase. No tocas código existente.

EN NUESTRO PROYECTO:"

───────────────────────────────────────────────────────────────────────────────

💻 CÓDIGO - STRATEGY: Estructura Modular (1 minuto)
───────────────────────────────────────────────────────────────────────────────

"[ABRIR CARPETA]

Archivo: services/inventario_strategies/

Este patrón STRATEGY está organizado DE FORMA MODULAR:

[MOSTRAR ESTRUCTURA EN VS CODE]

  inventario_strategies/
  ├── entrada/          → Estrategia de ENTRADA
  ├── salida/           → Estrategia de SALIDA
  └── ajuste/           → Estrategia de AJUSTE

Cada estrategia tiene su PROPIA CARPETA con componentes atómicos:

  ├── validar_*.py      → Validación
  ├── (operacion).py    → Operación (suma, resta, asigna)
  ├── registrar_*.py    → Persistencia en BD
  └── *_strategy.py     → Clase orquestadora

VENTAJA: Cada responsabilidad está SEPARADA en archivos únicos de ~30 líneas."

───────────────────────────────────────────────────────────────────────────────

💻 CÓDIGO - STRATEGY: EntradaStrategy (2 minutos)
───────────────────────────────────────────────────────────────────────────────

"[ABRIR CARPETA]

Archivo: services/inventario_strategies/entrada/

Aquí está la ESTRATEGIA DE ENTRADA dividida en 4 archivos:

[MOSTRAR ESTRUCTURA]

  entrada/
  ├── validar_entrada.py       (Validación)
  ├── sumar_stock.py           (Operación suma)
  ├── registrar_entrada.py     (Persistencia)
  └── entrada_strategy.py      (Orquestador)

[ABRIR entrada_strategy.py - Líneas 1-65]

EntradaStrategy():
  • Clase orquestadora (línea 18-65)
  • Método ejecutar() ORQUESTA el proceso
  • NO hace validación ni suma directamente, DELEGA

[MOSTRAR LÍNEA 39-62 - El método ejecutar()]

Ves cómo se llama a cada componente atómico:

  1. validar_entrada() → línea 40
  2. obtener producto → línea 46
  3. sumar_stock() → línea 49
  4. registrar_entrada() → línea 51-59

Cada paso es independiente. Puedes testear sumar_stock() SIN validación.

[ABRIR validar_entrada.py - Líneas 1-25]

Aquí está SOLO la validación:

  • validar_entrada(cantidad) - línea 9
  • validar_schema(...) - línea 17

RESPONSABILIDAD ÚNICA: Validar datos.

[ABRIR sumar_stock.py - Líneas 1-15]

RESPONSABILIDAD ÚNICA: Sumar

  def sumar_stock(producto, cantidad):
      producto.agregar_stock(cantidad)

Una línea de lógica. Testeable, simple, clara.

[ABRIR registrar_entrada.py - Líneas 1-30]

RESPONSABILIDAD ÚNICA: Persistencia

  def registrar_entrada(...):
      producto_repo.actualizar(producto)
      movimiento_repo.registrar_movimiento(...)

Guarda en BD. Nada más.

AHORA ENTIENDES la refactorización MODULAR del patrón STRATEGY."

───────────────────────────────────────────────────────────────────────────────

💻 CÓDIGO - STRATEGY: SalidaStrategy (2 minutos)
───────────────────────────────────────────────────────────────────────────────

"[ABRIR CARPETA]

Archivo: services/inventario_strategies/salida/

ESTRATEGIA DE SALIDA - dividida en 4 archivos:

  salida/
  ├── validar_salida.py        (Validación)
  ├── restar_stock.py          (Operación resta)
  ├── registrar_salida.py      (Persistencia)
  └── salida_strategy.py       (Orquestador)

[ABRIR salida_strategy.py - Líneas 1-75]

La DIFERENCIA CLAVE con ENTRADA está en validación:

[MOSTRAR línea 47-49]

  validar_salida(cantidad)
  validar_disponibilidad(producto, cantidad) ← ESTA FALTA EN ENTRADA

ESTA VALIDACIÓN es lo que diferencia Salida de Entrada.

[ABRIR validar_salida.py - Líneas 1-35]

Ves las funciones:

  • validar_salida(cantidad) - línea 8
  • validar_disponibilidad(producto, cantidad) - línea 14 ← CLAVE

validar_disponibilidad() VALIDA que hay suficiente stock:

  if cantidad > producto.stock:
      raise StockInsuficiente(...)

¿POR QUÉ esta diferencia? Porque en SALIDA no puedes dar más de lo que tienes.

[ABRIR restar_stock.py - Líneas 1-15]

Operación:

  def restar_stock(producto, cantidad):
      producto.reducir_stock(cantidad)

Análoga a sumar_stock pero resta.

AHORA VES LA DIFERENCIA: SalidaStrategy VALIDA; EntradaStrategy NO.
Mismo patrón, lógica diferente."

───────────────────────────────────────────────────────────────────────────────

💻 CÓDIGO - STRATEGY: AjusteStrategy (1 minuto 30 segundos)
───────────────────────────────────────────────────────────────────────────────

"[ABRIR CARPETA]

Archivo: services/inventario_strategies/ajuste/

ESTRATEGIA DE AJUSTE - dividida en 4 archivos:

  ajuste/
  ├── validar_ajuste.py        (Validación)
  ├── asignar_stock.py         (Operación asigna)
  ├── registrar_ajuste.py      (Persistencia)
  └── ajuste_strategy.py       (Orquestador)

[ABRIR ajuste_strategy.py - Líneas 1-65]

DIFERENCIA CON ENTRADA/SALIDA: Asigna valor EXACTO, no aritmética.

[MOSTRAR línea 45]

  asignar_stock(producto, nuevo_stock) ← No suma ni resta

Es una ASIGNACIÓN directa.

[ABRIR asignar_stock.py - Líneas 1-15]

Operación:

  def asignar_stock(producto, nuevo_stock):
      producto.establecer_stock(nuevo_stock)

Una línea. Sin cálculos. Valor exacto.

[ABRIR validar_ajuste.py - Líneas 1-10]

RESPONSABILIDAD ÚNICA: Validar que nuevo_stock >= 0

  if nuevo_stock < 0:
      raise DatosInvalidos(...)

Eso es todo. La validación de ajuste es simple.

¿VES EL PATRÓN? Las tres estrategias:

  1. EntradaStrategy → suma sin límite
  2. SalidaStrategy → resta con validación
  3. AjusteStrategy → asigna valor exacto

DIFERENTES algoritmos, MISMA interfaz, RESPONSABILIDADES separadas."

───────────────────────────────────────────────────────────────────────────────

💻 CÓDIGO - STRATEGY: Uso en API (1 minuto)
───────────────────────────────────────────────────────────────────────────────

"¿CÓMO se USAN estas estrategias?

[ABRIR ARCHIVO]

Archivo: api/v1/movimientos.py
Líneas: 80-120 (función entrada)

En el endpoint /entrada, ves:

[MOSTRAR CÓDIGO]

  strategy = ServiceContainer.get_entrada_strategy()
  resultado = strategy.ejecutar(
      producto_id=datos.get('producto_id'),
      cantidad=datos.get('cantidad'),
      ...
  )

El CLIENTE (API) NO conoce que Entrada está hecha de 4 archivos diferentes.
Solo ELIGE la estrategia y la EJECUTA.

TRANSPARENCIA: La arquitectura interna (modular) no afecta al cliente externo.

Si mañana cambias la validación de entrada, cambias:
  services/inventario_strategies/entrada/validar_entrada.py

El endpoint /entrada sigue siendo:

  strategy = ServiceContainer.get_entrada_strategy()
  resultado = strategy.ejecutar(...)

SIN CAMBIOS. Eso es ARCHITECTURE INDEPENDENCE."

───────────────────────────────────────────────────────────────────────────────

✅ RESUMEN - STRATEGY
───────────────────────────────────────────────────────────────────────────────

"STRATEGY PATTERN RESUELVE:

  ✓ Polimorfismo: Múltiples algoritmos, misma interfaz execute()
  ✓ Encapsulación: Cada estrategia es independiente
  ✓ Extensibilidad: Nueva estrategia = Nueva clase (sin tocar existentes)
  ✓ Testabilidad: Cada estrategia se prueba por separado

EN NUESTRO PROYECTO:
  • EntradaStrategy → Suma stock sin validación
  • SalidaStrategy → Resta stock con validación
  • AjusteStrategy → Asigna stock exacto

Tres algoritmos diferentes, misma interfaz. STRATEGY PATTERN.

[TRANSICIÓN]"

═════════════════════════════════════════════════════════════════════════════════
PATRÓN #4: OBSERVER
═════════════════════════════════════════════════════════════════════════════════

📖 EXPLICACIÓN (1 minuto 30 segundos)
───────────────────────────────────────────────────────────────────────────────

"CUARTO Y ÚLTIMO: OBSERVER PATTERN - Las Notificaciones.

¿CUÁL ES EL PROBLEMA?

Cuando algo importante OCURRE en tu aplicación (stock bajo, producto agotado), 
muchos OTROS SISTEMAS necesitan SABERLO:

  • Sistema de Alertas: ¡Avisa!
  • Sistema de Auditoría: ¡Registra!
  • Sistema de Notificaciones: ¡Envía email!

OPCIÓN 1 (MALA - Acoplamiento fuerte):

En la función que cambia stock, llamas:

  cambiar_stock()
    ├─ actualiza BD
    ├─ llamá AlertasService.alerta()
    ├─ llamá AuditoriaService.registra()
    ├─ llamá EmailService.envía()

Problemas:
  ✗ Stock manager CONOCE de alertas, auditoría, email (acoplado)
  ✗ Si agregás nuevo sistema, modificas cambiar_stock()
  ✗ Difícil de testear (dependencias internas)
  ✗ Violación de Single Responsibility

SOLUCIÓN - OBSERVER PATTERN:

Separas la lógica EN DOS:

  1. PUBLISHER (quién dispara evento): cambiar_stock()
  2. OBSERVERS (quiénes escuchan): AlertasListener, AuditoriaListener, etc

El Publisher NO conoce a los Observers. Solo DISPARA eventos.

Los Observers se REGISTRAN en un EventManager y ESCUCHAN.

Cuando ocurre un evento:

  cambiar_stock()
    ├─ actualiza BD
    └─ event_manager.emit(StockBajoEvent(...))

El EventManager notifica a TODOS los Observers registrados.

Observers reaccionan:
  ├─ AlertasListener: ¡Genera alerta!
  ├─ AuditoriaListener: ¡Registra en log!
  └─ NotificacionesListener: ¡Crea notificación!

¿Nuevos Observers? Solo registrás. Sin acoplar código.

EN NUESTRO PROYECTO (ACABO DE IMPLEMENTARLO):"

───────────────────────────────────────────────────────────────────────────────

💻 CÓDIGO - OBSERVER: Event (1 minuto)
───────────────────────────────────────────────────────────────────────────────

"[ABRIR ARCHIVO]

Archivo: core/event_system/event.py
Líneas: 1-70

Primero, definimos LOS EVENTOS que pueden ocurrir:

[MOSTRAR CÓDIGO]

Tenemos:
  • Event: clase base
  • StockBajoEvent: cuando stock < mínimo
  • ProductoAgotadoEvent: cuando stock == 0
  • MovimientoRegistradoEvent: cuando se registra movimiento

Cada evento encapsula la información relevante.

Ej. StockBajoEvent contiene:
  - producto_id
  - nombre
  - stock actual
  - stock mínimo"

───────────────────────────────────────────────────────────────────────────────

💻 CÓDIGO - OBSERVER: Observer Interface (30 segundos)
───────────────────────────────────────────────────────────────────────────────

"[ABRIR ARCHIVO]

Archivo: core/event_system/observer.py

Aquí definimos qué TIENE QUE HACER todo Observer:

[MOSTRAR CÓDIGO]

  class Observer(ABC):
      @abstractmethod
      def update(self, event: Event) -> None:
          pass

CUALQUIER Observer debe implementar update(event).

Cuando ocurre un evento, se llama a update()."

───────────────────────────────────────────────────────────────────────────────

💻 CÓDIGO - OBSERVER: EventManager (1 minuto 30 segundos)
───────────────────────────────────────────────────────────────────────────────

"[ABRIR ARCHIVO]

Archivo: core/event_system/event_manager.py
Líneas: 1-80

EventManager es el COORDINATOR. Tres responsabilidades:

[MOSTRAR CÓDIGO]

1️⃣  SUBSCRIBE (línea 20-35): Los Observers se REGISTRAN aquí
  
  event_manager.subscribe('stock_bajo', alertas_listener)

2️⃣  UNSUBSCRIBE (línea 37-45): Los Observers se DESREGISTRAN

3️⃣  EMIT (línea 47-60): El Publisher DISPARA eventos
  
  event_manager.emit(StockBajoEvent(...))

Cuando emite, EventManager notifica a TODOS los Observers registrados para 
ese tipo de evento."

───────────────────────────────────────────────────────────────────────────────

💻 CÓDIGO - OBSERVER: Listeners Concretos (2 minutos)
───────────────────────────────────────────────────────────────────────────────

"[ABRIR ARCHIVO]

Archivo: core/event_system/listeners.py
Líneas: 1-150

Aquí están los OBSERVERS CONCRETOS que reaccionan a eventos.

[MOSTRAR CLASE AlertasListener]

1️⃣  AlertasListener (línea 10-35):

Implementa el método update() que genera ALERTAS:

  • Si ocurre StockBajoEvent → alerta de stock bajo: ⚠️
  • Si ocurre ProductoAgotadoEvent → alerta crítica: 🔴

[SCROLL]

2️⃣  AuditoriaListener (línea 40-60):

Registra EVENTOS en un log de auditoría:

  • Cada evento se guarda con timestamp
  • Puedes consultar: listener.obtener_auditoria()

[SCROLL]

3️⃣  NotificacionesListener (línea 65-150):

Genera NOTIFICACIONES en diferentes formatos:

  • stock_bajo → notificación tipo 'advertencia'
  • producto_agotado → notificación tipo 'error'
  • movimiento_registrado → notificación tipo 'info'

Cada listener maneja SU responsabilidad. Sin acoplamiento."

───────────────────────────────────────────────────────────────────────────────

💻 CÓDIGO - OBSERVER: Uso/Setup (1 minuto)
───────────────────────────────────────────────────────────────────────────────

"¿CÓMO SE CONFIGURA el sistema Observer?

Durante la inicialización de la app, registramos los listeners:

[PSEUDO-CÓDIGO]

  from core.event_system import (
      event_manager,
      AlertasListener,
      AuditoriaListener,
      NotificacionesListener,
  )

  # Crear instancias de listeners
  alertas = AlertasListener()
  auditoria = AuditoriaListener()
  notificaciones = NotificacionesListener()

  # Registrar en EventManager
  event_manager.subscribe('stock_bajo', alertas)
  event_manager.subscribe('stock_bajo', auditoria)
  event_manager.subscribe('stock_bajo', notificaciones)

Ahora, cuando CUALQUIER parte del código dispara:

  event_manager.emit(StockBajoEvent(...))

AUTOMÁTICAMENTE se ejecutan:
  ├─ alertas.update()
  ├─ auditoria.update()
  └─ notificaciones.update()

Sin acoplamientos. Limpio."

───────────────────────────────────────────────────────────────────────────────

✅ RESUMEN - OBSERVER
───────────────────────────────────────────────────────────────────────────────

"OBSERVER PATTERN RESUELVE:

  ✓ Desacoplamiento: Publisher NO conoce Observers
  ✓ Reactividad: Cambios automáticos se propagan
  ✓ Extensibilidad: Nuevos Observers sin modificar código existente
  ✓ Separación de concerns: Cada Observer maneja su responsabilidad

EN NUESTRO PROYECTO:
  • EventManager → Coordinator (Publisher/Subscriber)
  • AlertasListener → Genera alertas visuales
  • AuditoriaListener → Registra eventos
  • NotificacionesListener → Crea notificaciones

Cuando stock cae bajo el mínimo, AUTOMÁTICAMENTE:
  🔔 Se genera alerta
  📝 Se registra en auditoría
  📧 Se crea notificación

OBSERVER PATTERN."

═════════════════════════════════════════════════════════════════════════════════
⚡ COMPARACIÓN VISUAL - LOS 4 PATRONES JUNTOS (2 minutos)
═════════════════════════════════════════════════════════════════════════════════

"Ahora veamos cómo estos 4 patrones TRABAJAN JUNTOS en el proyecto:

[MOSTRAR DIAGRAMA O EXPLICACIÓN NARRATIVA]

FLUJO DE UNA OPERACIÓN:

1. Usuario hace POST /api/v1/movimientos/salida

2. FACTORY METHOD se activa:
   - Crea estrategia: strategy = ServiceContainer.get_salida_strategy()
   
3. STRATEGY se ejecuta:
   - SalidaStrategy valida y resta stock

4. OBSERVER se dispara:
   - Si stock cae bajo mínimo → StockBajoEvent
   - event_manager.emit(StockBajoEvent(...))
   
5. OBSERVER listeners reaccionan:
   - AlertasListener: ⚠️ 'Stock bajo!'
   - AuditoriaListener: 📝 Registra
   - NotificacionesListener: 📧 Notifica

6. TODO coordinado por FACADE:
   - FlaskApplication orquesta app
   - DatabaseManager orquesta BD

CUATRO PATRONES, UNA OPERACIÓN SIMPLE.

Cada patrón resuelve un problema diferente:
  • FACADE → Complejidad
  • FACTORY → Creación
  • STRATEGY → Algoritmos intercambiables
  • OBSERVER → Reactividad desacoplada

═════════════════════════════════════════════════════════════════════════════════
🎯 CONCLUSIÓN (30 segundos)
═════════════════════════════════════════════════════════════════════════════════

"Estos patrones de diseño no son académicos. Son HERRAMIENTAS PRÁCTICAS que 
hacen tu código:

  ✓ Más mantenible
  ✓ Más testeable
  ✓ Más escalable
  ✓ Menos acoplado
  ✓ Más profesional

En este proyecto ves cómo se aplican en un CONTEXTO REAL. La próxima vez que 
códigos, piensa en estos patrones.

¿Necesitás opciones intercambiables? → STRATEGY
¿Tenés subsistemas complejos? → FACADE
¿Centralizás creación? → FACTORY METHOD
¿Necesitás reactividad? → OBSERVER

Gracias por ver. Cuéntame en comentarios qué patrón te pareció más interesante.

Hasta la próxima! 👋"

═════════════════════════════════════════════════════════════════════════════════

───────────────────────────────────────────────────────────────────────────────
📋 NOTAS PARA EL QUE GRABA:
───────────────────────────────────────────────────────────────────────────────

ARCHIVOS A TENER ABIERTOS EN VS CODE (en orden):

1. app/application.py (líneas 1-80) - FACADE #1
2. database/__init__.py (líneas 1-150) - FACADE #2
3. app/__init__.py (líneas 14-30) - FACTORY METHOD #1
4. infrastructure/repositories/repositorio_factory/__init__.py - FACTORY #2
5. services/inventario_strategies/entrada/entrada_strategy.py - STRATEGY Entrada
6. services/inventario_strategies/entrada/validar_entrada.py - STRATEGY Entrada Validación
7. services/inventario_strategies/salida/salida_strategy.py - STRATEGY Salida
8. services/inventario_strategies/salida/validar_salida.py - STRATEGY Salida (con disponibilidad)
9. services/inventario_strategies/ajuste/ajuste_strategy.py - STRATEGY Ajuste
10. api/v1/movimientos.py (líneas 80-260) - STRATEGY USO EN API
11. core/event_system/event.py (líneas 1-70) - OBSERVER Event
12. core/event_system/observer.py - OBSERVER Interface
13. core/event_system/event_manager.py (líneas 1-80) - OBSERVER Manager
14. core/event_system/listeners.py (líneas 1-150) - OBSERVER Listeners

TIMING:
- FACADE: 3-4 minutos
- FACTORY: 3-4 minutos
- STRATEGY: 4-5 minutos
- OBSERVER: 4-5 minutos
- Conclusión: 1 minuto
- TOTAL: ~15-17 minutos

SUGERENCIAS DE PRESENTACIÓN:
- Usar tema oscuro de VS Code (mejor para video)
- Aumentar tamaño de fuente (mínimo 16-18pt)
- Pausar después de cada patrón (dar tiempo al viewers para asimilar)
- No scrollear rápido (dejar leer el código)
- Destacar con hover las líneas importantes
