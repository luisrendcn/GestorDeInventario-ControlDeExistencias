"""
╔════════════════════════════════════════════════════════════════════════════╗
║       ARCHIVO: infrastructure/database/connection_manager/desconectar.py   ║
║       RESPONSABILIDAD: Desconectar de la Base de Datos                    ║
╚════════════════════════════════════════════════════════════════════════════╝

🎯 ÚNICA RESPONSABILIDAD:
   Cerrar conexión a SQLite de forma segura.
"""


class DesconectarMixin:
    """
    Mixin que agrega método para desconectar de la BD.
    
    RESPONSABILIDAD: 1
    • Cerrar conexión SQLite de forma segura
    
    Requiere atributo:
        • self.conn (conexión SQLite)
    """
    
    def desconectar(self):
        """
        🔌 Cerrar conexión a BD.
        
        Cierra conexión e inmediatamente asigna conn = None.
        Idempotente - puede llamarse múltiples veces sin error.
        """
        try:
            if self.conn:
                self.conn.close()
                self.conn = None
                print("[DB] Desconectado")
        except Exception as e:
            print(f"[DB] Error al desconectar: {e}")
    
    def cerrar(self):
        """Alias para desconectar()."""
        self.desconectar()
