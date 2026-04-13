"""
╔════════════════════════════════════════════════════════════════╗
║  ARCHIVO: api/v1/__init__.py                                   ║
║  FUNCIÓN: Orquestador de blueprints y rutas de API V1         ║
╚════════════════════════════════════════════════════════════════╝

📋 RESPONSABILIDADES DEL ARCHIVO:
  • Centralizar creación de servicios (inyección de dependencias)
  • Importar factory de repositorios
  • Crear blueprints individuales para cada dominio
  • Registrar blueprints en la aplicación Flask
  • Configurar prefijo de URL (/api/v1)

🏗️  ARQUITECTURA DE BLUEPRINTS V1:
  
  api/v1/
    ├─ productos.py    → CRUD Producto
    ├─ movimientos.py  → Estrategias de stock (ENTRADA, SALIDA, AJUSTE)
    ├─ reportes.py     → Análisis e informes
    ├─ admin.py        → Inicialización y limpieza
    └─ errors.py       → Manejadores globales de errores

📡 RUTAS PUBLICADAS (15 total):
  
  GET    /api/v1/productos                   (listar todos)
  GET    /api/v1/productos/<id>              (obtener uno)
  POST   /api/v1/productos                   (crear)
  DELETE /api/v1/productos/<id>              (eliminar)
  
  POST   /api/v1/entrada                     (STRATEGY: Entrada stock)
  POST   /api/v1/salida                      (STRATEGY: Salida stock)
  POST   /api/v1/ajuste                      (STRATEGY: Ajuste manual)
  
  GET    /api/v1/reporte                     (reporte general)
  GET    /api/v1/alertas                     (alertas de bajo stock)
  GET    /api/v1/historial                   (historial movimientos)
  GET    /api/v1/productos-mayor-stock       (products con más stock)
  GET    /api/v1/productos-menor-stock       (products con menos stock)
  
  POST   /api/v1/inicializar                 (admin: cargar demo)
  POST   /api/v1/limpiar                     (admin: limpiar BD)

🔗 INYECCIÓN DE DEPENDENCIAS:
  
  RepositorioFactory
    ↓
  ProductoService ────┐
  InventarioService  ├─→ Blueprints
  ReporteService  ───┘
"""

from flask import Flask
from .productos import crear_productos_bp
from .movimientos import crear_movimientos_bp
from .reportes import crear_reportes_bp
from .admin import crear_admin_bp


def crear_blueprints_v1(app: Flask):
    """
    🔨 Orquestar creación e inyección de blueprints V1.
    
    RESPONSABILIDADES (1):
      1️⃣  Crear y registrar blueprints en Flask
          ├─ Llamar crear_X_bp() para cada dominio
          ├─ app.register_blueprint(..., url_prefix='/api/v1')
          └─ Loop para todos los blueprints
    
    NOTA: Los servicios se instancian a través de ServiceContainer (lazy)
    
    FLUJO DE LLAMADA:
        app.py
          ↓
          init_database(db_path)
            ├─ ConnectionManager.conectar()
            ├─ SchemaInitializer.crear_tablas()
            └─ DatabaseStore.set_database(conn)
          ↓
          registrar_blueprints(app)
            ↓
          crear_blueprints_v1(app)
    
    DEPENDENCIAS:
        • app (Flask): Aplicación Flask ya creada
        • DatabaseStore: Debe tener set_database() llamado antes
        • ServiceContainer: Instancia servicios bajo demanda
    
    LADO EFFECTS:
        • Modifica app.blueprints (agrega blueprints)
        • Registra rutas en app
    """
    
    # Crear y registrar blueprints (ahora sin inyección, usan ServiceContainer)
    print("[BLUEPRINTS] Creando blueprint produtos...")
    productos_bp = crear_productos_bp()
    print("[BLUEPRINTS] ✓ productos_bp creado")
    
    print("[BLUEPRINTS] Creando blueprint movimientos...")
    movimientos_bp = crear_movimientos_bp()
    print("[BLUEPRINTS] ✓ movimientos_bp creado")
    
    print("[BLUEPRINTS] Creando blueprint reportes...")
    reportes_bp = crear_reportes_bp()
    print("[BLUEPRINTS] ✓ reportes_bp creado")
    
    print("[BLUEPRINTS] Creando blueprint admin...")
    admin_bp = crear_admin_bp()
    print("[BLUEPRINTS] ✓ admin_bp creado")
    
    # Registrar
    print("[BLUEPRINTS] Registrando blueprints...")
    app.register_blueprint(productos_bp, url_prefix='/api/v1')
    print("[BLUEPRINTS] ✓ productos registrado")
    
    app.register_blueprint(movimientos_bp, url_prefix='/api/v1')
    print("[BLUEPRINTS] ✓ movimientos registrado")
    
    app.register_blueprint(reportes_bp, url_prefix='/api/v1')
    print("[BLUEPRINTS] ✓ reportes registrado")
    
    app.register_blueprint(admin_bp, url_prefix='/api/v1')
    print("[BLUEPRINTS] ✓ admin registrado")
    
    print("[BLUEPRINTS] ✅ Todos los blueprints registrados correctamente")


__all__ = ['crear_blueprints_v1']
