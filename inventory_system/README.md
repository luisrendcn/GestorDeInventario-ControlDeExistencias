# Módulo de Gestión de Inventario

Sistema profesional de gestión de inventario desarrollado en Python puro, aplicando principios SOLID, patrones de diseño y arquitectura limpia.

---

## Características

- Gestión completa de productos (crear, editar, eliminar, listar, buscar)
- Soporte para tres tipos de productos: Simple, Perecedero y Digital
- Registro de ventas (reduce stock) y compras (aumenta stock)
- Historial de transacciones con totales
- Alertas automáticas de stock bajo y stock agotado
- Log de eventos de stock en tiempo real
- Estadísticas del sistema (valor del inventario, balance ventas/compras)
- Interfaz de línea de comandos interactiva y clara
- Sin dependencias externas — solo Python 3.8+

---

## Estructura del Proyecto

```
inventory_system/
│
├── main.py                         # Punto de entrada
│
├── models/                         # Clases de dominio
│   ├── __init__.py
│   ├── producto.py                 # Producto (abstracto), ProductoSimple, ProductoPerecedero, ProductoDigital
│   ├── inventario.py               # Repositorio en memoria de productos
│   └── transaccion.py              # Modelo de ventas y compras
│
├── services/                       # Lógica de negocio
│   ├── __init__.py
│   ├── inventario_service.py       # Coordina stock, notificaciones y transacciones
│   └── transaccion_service.py      # Gestiona el historial de movimientos
│
├── controllers/                    # Flujo de la aplicación (CLI)
│   ├── __init__.py
│   └── menu_controller.py          # Menú interactivo principal
│
├── patterns/                       # Implementación de patrones de diseño
│   ├── __init__.py
│   ├── factory.py                  # Factory Method — creación de productos
│   ├── facade.py                   # Facade — interfaz simplificada del sistema
│   └── observer.py                 # Observer — notificaciones de cambios de stock
│
├── utils/                          # Utilidades reutilizables
│   ├── __init__.py
│   ├── formato.py                  # Formateo de salida en consola
│   └── validacion.py               # Lectura y validación de inputs del usuario
│
└── README.md
```

---

## Cómo Ejecutar

```bash
cd inventory_system
python main.py
```

Requiere Python 3.8 o superior. No necesita instalar ninguna librería adicional.

---

## Patrones de Diseño Aplicados

### 1. Factory Method (Creacional) — `patterns/factory.py`

**Problema:** El sistema necesita crear distintos tipos de productos sin que el código cliente conozca los constructores concretos.

**Solución:** Cada tipo de producto tiene su propia fábrica concreta que extiende `ProductoFactory`. El `FactoryManager` actúa como selector, eligiendo la fábrica correcta según el tipo indicado.

```
ProductoFactory (abstracta)
    ├── ProductoSimpleFactory     → crea ProductoSimple
    ├── ProductoPerecederoFactory → crea ProductoPerecedero
    └── ProductoDigitalFactory    → crea ProductoDigital

FactoryManager.crear_producto("perecedero", datos)
```

**Dónde se usa:** En `SistemaInventarioFacade.crear_producto()` — el cliente solo indica el tipo y los datos, sin instanciar directamente ninguna clase concreta.

**Beneficio:** Agregar un nuevo tipo de producto (`ProductoLote`, `ProductoUsado`) solo requiere crear una nueva fábrica y registrarla, sin tocar código existente (OCP).

---

### 2. Facade (Estructural) — `patterns/facade.py`

**Problema:** El sistema tiene múltiples subsistemas (`Inventario`, `InventarioService`, `TransaccionService`, `SujetoStock`, `FactoryManager`). El controlador CLI no debería conocer ni coordinar todos estos componentes.

**Solución:** `SistemaInventarioFacade` expone una interfaz simple y unificada que internamente coordina todos los subsistemas.

```
MenuController (CLI)
    └── SistemaInventarioFacade
            ├── Inventario
            ├── InventarioService
            ├── TransaccionService
            ├── SujetoStock (Observer)
            └── FactoryManager
```

**Dónde se usa:** En `MenuController` — todas las operaciones se realizan a través del facade. El controlador solo llama métodos como `facade.registrar_venta(id, cantidad)` sin preocuparse de cómo funciona internamente.

**Beneficio:** Bajo acoplamiento entre la interfaz de usuario y los subsistemas. Facilita cambiar la implementación interna sin modificar el controlador.

---

### 3. Observer (Comportamental) — `patterns/observer.py`

**Problema:** Cuando el stock cambia (por una venta o compra), varios subsistemas necesitan reaccionar: mostrar alertas en consola, registrar logs. Sin el patrón, habría que llamar manualmente a cada subsistema desde el servicio de inventario.

**Solución:** `SujetoStock` mantiene una lista de observadores. Cuando ocurre un cambio de stock, notifica a todos automáticamente.

```
SujetoStock (publicador)
    ├── AlertaConsolaObservador      → imprime alertas de stock bajo
    ├── AlertaStockCriticoObservador → alerta cuando el stock llega a 0
    └── LogObservador                → registra el historial de eventos
```

**Dónde se usa:** En `InventarioService.registrar_venta()` y `registrar_compra()` — después de modificar el stock, se llama a `sujeto.notificar(producto, evento, cantidad)`. Cada observador reacciona de forma independiente.

**Beneficio:** Agregar un nuevo observador (p. ej. `EmailObservador`, `SlackObservador`) solo requiere implementar la interfaz `ObservadorStock` y suscribirse al sujeto, sin modificar el código existente.

---

## Principios SOLID Aplicados

| Principio | Aplicación en el proyecto |
|-----------|---------------------------|
| **SRP** (Responsabilidad Única) | Cada clase tiene una única razón para cambiar. `Inventario` solo gestiona la colección, `TransaccionService` solo el historial, `MenuController` solo la UI. |
| **OCP** (Abierto/Cerrado) | `FactoryManager.registrar_fabrica()` permite extender tipos de producto sin modificar el código existente. Los nuevos observadores se suscriben sin cambiar `SujetoStock`. |
| **LSP** (Sustitución de Liskov) | `ProductoSimple`, `ProductoPerecedero` y `ProductoDigital` son intercambiables donde se usa `Producto`. |
| **ISP** (Segregación de Interfaces) | `ObservadorStock` y `ProductoFactory` son interfaces pequeñas y específicas. |
| **DIP** (Inversión de Dependencias) | `InventarioService` depende de la abstracción `SujetoStock`, no de observadores concretos. |

---

## Ejemplo de Flujo Completo

```
1. Usuario selecciona "Crear Producto" → tipo: perecedero
2. MenuController captura datos y llama facade.crear_producto("perecedero", datos)
3. Facade llama FactoryManager.crear_producto() → ProductoPerecederoFactory crea el objeto
4. Facade agrega el producto al Inventario

5. Usuario selecciona "Registrar Venta" → ID: ALIM001, cantidad: 48
6. Facade llama inventario_service.registrar_venta()
7. El servicio reduce el stock del producto (quedan 2 < mínimo de 10)
8. El servicio notifica: sujeto.notificar(producto, "venta", 48)
9. Los observadores actúan:
   - AlertaConsolaObservador imprime ⚠ ALERTA DE STOCK BAJO
   - LogObservador registra el evento en el historial
```

---

## Datos de Demostración

Al iniciar el sistema se cargan 6 productos de ejemplo:

| ID      | Nombre              | Tipo        | Stock | Mín |
|---------|---------------------|-------------|-------|-----|
| ELEC001 | Laptop HP 15        | Simple      | 10    | 3   |
| ELEC002 | Mouse Logitech M705 | Simple      | 4     | 5   |
| ALIM001 | Yogur Natural       | Perecedero  | 50    | 10  |
| ALIM002 | Leche Entera 1L     | Perecedero  | 3     | 20  |
| SOFT001 | Licencia Office 365 | Digital     | 20    | 5   |
| SOFT002 | Adobe Photoshop     | Digital     | 2     | 3   |

Los productos ELEC002, ALIM002 y SOFT002 comienzan con stock bajo para demostrar las alertas.

---

## Decisiones de Diseño

- **abc (Abstract Base Classes):** Se usan para definir contratos claros entre capas. `Producto`, `ProductoFactory` y `ObservadorStock` son abstractas para garantizar que las subclases implementen la interfaz esperada.
- **Repositorio en memoria:** `Inventario` usa un diccionario (`dict`) para acceso O(1) por ID. Podría reemplazarse por una base de datos sin cambiar el resto del sistema.
- **UUID para transacciones:** Las transacciones usan UUID cortos para garantizar IDs únicos sin estado global.
- **Separación clara de capas:** `models` no conoce `services`, `services` no conoce `controllers`, `controllers` solo habla con `patterns/facade`. Esta jerarquía evita dependencias circulares y facilita el testing.
