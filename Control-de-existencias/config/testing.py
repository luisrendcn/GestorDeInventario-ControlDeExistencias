"""
╔════════════════════════════════════════════════════════════════════════════╗
║                  ARCHIVO: config/testing.py                               ║
║                  FUNCIÓN: Configuración para ambiente TESTING              ║
╚════════════════════════════════════════════════════════════════════════════╝

📋 RESPONSABILIDAD DEL ARCHIVO (1):
   Definir overrides de configuración específicos para TESTING

═════════════════════════════════════════════════════════════════════════════

📦 CONTENIDO:

┌─ class TestingConfig(Config) (RESPONSABILIDAD: 1)
│  └─ Responsabilidad: Override valores base para ambiente de testing
│
│  Cambios vs Config base:
│  • TESTING = True (modo testing)
│  • DEBUG = False (evitar hot-reload durante tests)
│  • DATABASE_PATH = ':memory:' (BD en memoria para rapidez)
│  • DATABASE_URL = 'sqlite:///:memory:' (conexión en memoria)
"""

from config.base import Config


class TestingConfig(Config):
    """
    Configuración específica para TESTING.
    
    RESPONSABILIDAD (1):
      1️⃣  Override valores base con configuración de testing
    
    Cambios realizados:
      • TESTING = True: Habilita modo testing
      • DEBUG = False: Evita hot-reload y features de desarrollo
      • DATABASE_PATH = ':memory:': BD en memoria para tests rápidos
      • DATABASE_URL = 'sqlite:///:memory:': Conexión en memoria
    
    Ambiente: Ideal para ejecutar tests rápidos sin I/O de disco
    Ventajas:
      • Tests más rápidos (sin I/O)
      • Aislamiento entre tests (cada uno con BD nueva)
      • Limpieza automática (desaparece cuando termina)
    """
    
    TESTING = True
    DEBUG = False
    DATABASE_PATH = ':memory:'
    DATABASE_URL = 'sqlite:///:memory:'
