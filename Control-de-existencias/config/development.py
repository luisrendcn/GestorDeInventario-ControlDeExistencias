"""
╔════════════════════════════════════════════════════════════════════════════╗
║                  ARCHIVO: config/development.py                           ║
║                  FUNCIÓN: Configuración para ambiente DESARROLLO           ║
╚════════════════════════════════════════════════════════════════════════════╝

📋 RESPONSABILIDAD DEL ARCHIVO (1):
   Definir overrides de configuración específicos para DESARROLLO

═════════════════════════════════════════════════════════════════════════════

📦 CONTENIDO:

┌─ class DevelopmentConfig(Config) (RESPONSABILIDAD: 1)
│  └─ Responsabilidad: Override valores base para ambiente de desarrollo
│
│  Cambios vs Config base:
│  • DEBUG = True (para hot-reload y error details)
│  • TESTING = False (desarrollo real, no testing)
│  • DATABASE_PATH sigue siendo archivo (no en memoria)
"""

from config.base import Config


class DevelopmentConfig(Config):
    """
    Configuración específica para DESARROLLO.
    
    RESPONSABILIDAD (1):
      1️⃣  Override valores base con configuración de desarrollo
    
    Cambios realizados:
      • DEBUG = True: Habilita hot-reload, debug bar, error details
      • TESTING = False: Usa BD real, no en memoria
      • DATABASE_PATH: Sigue siendo archivo SQLite normal
    
    Ambiente: Ideal para desarrollo local con servidor Flask corriendo
    """
    
    DEBUG = True
    TESTING = False
