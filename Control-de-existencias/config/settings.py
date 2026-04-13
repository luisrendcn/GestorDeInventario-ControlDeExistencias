"""
╔════════════════════════════════════════════════════════════════════════════╗
║                  ARCHIVO: config/settings.py                              ║
║                  FUNCIÓN: Selector de configuración por ambiente           ║
╚════════════════════════════════════════════════════════════════════════════╝

📋 RESPONSABILIDAD DEL ARCHIVO (1):
   Seleccionar y exponer la configuración correcta basada en el ambiente

═════════════════════════════════════════════════════════════════════════════

📦 LÓGICA:

1. Leer variable ENV del sistema (default: 'development')
2. Importar la clase de configuración correspondiente:
   • ENV='production' → ProductionConfig
   • ENV='testing' → TestingConfig
   • ENV='development' → DevelopmentConfig (default)
3. Instanciar y exportar como `config`

═════════════════════════════════════════════════════════════════════════════

📂 ESTRUCTURA DE ARCHIVOS:

config/
├─ base.py           → Config (base común)
├─ development.py    → DevelopmentConfig(Config)
├─ testing.py        → TestingConfig(Config)
├─ production.py     → ProductionConfig(Config)
├─ settings.py       → Selector (este archivo)
└─ __init__.py       → Exports para facilitar imports
"""

import os
from config.base import Config
from config.development import DevelopmentConfig
from config.testing import TestingConfig
from config.production import ProductionConfig


# ═══════════════════════════════════════════════════════════════════════════
# SELECTOR DE AMBIENTE
# ═══════════════════════════════════════════════════════════════════════════

ENV = os.getenv('ENV', 'development')

if ENV == 'production':
    config = ProductionConfig()
elif ENV == 'testing':
    config = TestingConfig()
else:
    # Default: development
    config = DevelopmentConfig()


# ═══════════════════════════════════════════════════════════════════════════
# EXPORTS (para facilitar imports desde app.py)
# ═══════════════════════════════════════════════════════════════════════════

__all__ = ['config', 'Config', 'DevelopmentConfig', 'TestingConfig', 'ProductionConfig']

