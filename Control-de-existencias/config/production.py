"""
╔════════════════════════════════════════════════════════════════════════════╗
║                  ARCHIVO: config/production.py                            ║
║                  FUNCIÓN: Configuración para ambiente PRODUCCIÓN           ║
╚════════════════════════════════════════════════════════════════════════════╝

📋 RESPONSABILIDAD DEL ARCHIVO (1):
   Definir overrides de configuración específicos para PRODUCCIÓN

═════════════════════════════════════════════════════════════════════════════

📦 CONTENIDO:

┌─ class ProductionConfig(Config) (RESPONSABILIDAD: 1)
│  └─ Responsabilidad: Override valores base para ambiente de producción
│
│  Cambios vs Config base:
│  • DEBUG = False (nunca debug en producción)
│  • TESTING = False (nunca testing en producción)
│  • DATABASE_PATH sigue siendo archivo (base de datos real en servidor)
"""

from config.base import Config


class ProductionConfig(Config):
    """
    Configuración específica para PRODUCCIÓN.
    
    RESPONSABILIDAD (1):
      1️⃣  Override valores base con configuración de producción
    
    Cambios realizados:
      • DEBUG = False: NUNCA activar debug en producción
      • TESTING = False: No usar modo testing
      • DATABASE_PATH: Archivo SQLite en servidor real
      • SECRET_KEY: DEBE ser overrideado por env var en producción
    
    Ambiente: Servidor de producción con datos reales
    
    ⚠️  IMPORTANTE:
        • Cambiar SECRET_KEY en archivo .env de producción
        • Usar versión de SQLite optimizada para producción
        • Considerarasí usar PostgreSQL en lugar de SQLite
        • Configurar logs apropiados
    """
    
    DEBUG = False
    TESTING = False
