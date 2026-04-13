"""
╔════════════════════════════════════════════════════════════════════════════╗
║   ARCHIVO: database_store/get_database.py                                 ║
║   RESPONSABILIDAD: Obtener conexión BD global                             ║
╚════════════════════════════════════════════════════════════════════════════╝

🎯 ÚNICA RESPONSABILIDAD:
   Recuperar la conexión BD con reconexión automática.
"""

import sqlite3


class GetDatabaseMixin:
    """
    Mixin que agrega método para obtener conexión.
    
    RESPONSABILIDAD: 1
    • Recuperar conexión BD con reconexión automática si está cerrada
    """
    
    @classmethod
    def get_database(cls):
        """
        Obtener la conexión BD global.
        
        Con reconexión automática si la conexión está cerrada.
        
        Returns:
            Conexión SQLite
        
        Raises:
            RuntimeError: Si no está inicializada
        """
        if cls._conn is None or not hasattr(cls, '_db_path') or cls._db_path is None:
            raise RuntimeError("Database no inicializada")
        
        # Intentar usar la conexión
        try:
            cls._conn.execute("SELECT 1")
            return cls._conn
        except sqlite3.ProgrammingError as e:
            if "closed" in str(e).lower():
                # Reconectar
                print(f"[DB] Reconectando automáticamente...")
                try:
                    cls._conn = sqlite3.connect(cls._db_path, check_same_thread=False)
                    cls._conn.row_factory = sqlite3.Row
                    print(f"[DB] ✓ Reconectado")
                    return cls._conn
                except Exception as err:
                    raise RuntimeError(f"Reconexión fallida: {err}")
            raise RuntimeError(f"Database error: {e}")
        except Exception as e:
            raise RuntimeError(f"Database error: {e}")
