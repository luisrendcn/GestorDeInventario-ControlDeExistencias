"""
╔════════════════════════════════════════════════════════════════════════════╗
║       ARCHIVO: infrastructure/database/schema_initializer/crear_tablas.py  ║
║       RESPONSABILIDAD: Crear tablas de la Base de Datos                   ║
╚════════════════════════════════════════════════════════════════════════════╝

🎯 ÚNICA RESPONSABILIDAD:
   Ejecutar CREATE TABLE IF NOT EXISTS para inicializar esquema.
"""


class CrearTablasMixin:
    """
    Mixin que agrega método para crear tablas.
    
    RESPONSABILIDAD: 1
    • Ejecutar CREATE TABLE IF NOT EXISTS
    
    Requiere atributo:
        • self.conn (conexión SQLite)
    """
    
    def crear_tablas(self):
        """
        🔧 Crear tablas si no existen.
        
        Flujo:
            1. CREATE TABLE productos (catálogo)
            2. CREATE TABLE movimientos (auditoría)
            3. Commit
        
        Nota: CREATE TABLE IF NOT EXISTS es idempotente
        """
        cursor = self.conn.cursor()
        
        # Tabla de productos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                id TEXT PRIMARY KEY,
                nombre TEXT NOT NULL,
                precio REAL NOT NULL,
                stock INTEGER NOT NULL DEFAULT 0,
                stock_minimo INTEGER NOT NULL DEFAULT 5,
                descripcion TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Tabla de movimientos (auditoría)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS movimientos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                producto_id TEXT NOT NULL,
                tipo TEXT NOT NULL,
                cantidad INTEGER NOT NULL,
                stock_anterior INTEGER,
                stock_nuevo INTEGER,
                motivo TEXT,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE CASCADE
            )
        """)
        
        self.conn.commit()
        print("[DB] Tablas creadas/verificadas")
