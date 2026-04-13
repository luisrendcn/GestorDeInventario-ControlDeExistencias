"""
╔════════════════════════════════════════════════════════════════════════════╗
║                  ARCHIVO: config/base.py                                  ║
║                  FUNCIÓN: Configuración base común                        ║
╚════════════════════════════════════════════════════════════════════════════╝

📋 RESPONSABILIDAD DEL ARCHIVO (1):
   Definir configuración base común a TODOS los ambientes

═════════════════════════════════════════════════════════════════════════════

📦 CONTENIDO:

┌─ class Config (RESPONSABILIDAD: 1)
│  └─ Responsabilidad: Proporcionar valores base compartidos por todos
│     los ambientes (desarrollo, testing, producción)
│
│  Atributos:
│  • SECRET_KEY - Clave secreta Flask (sensible a SECRET_KEY env)
│  • DEBUG - Modo debug (sensible a DEBUG env)
│  • TESTING - Modo testing
│  • DATABASE_PATH - Ruta DB SQLite (sensible a DB_PATH env)
│  • DATABASE_URL - Connection string
│  • JSON_SORT_KEYS - Formateo JSON
│  • JSONIFY_PRETTYPRINT_REGULAR - Formateo JSON
│  • CORS_ORIGINS - Orígenes permitidos (sensible a CORS_ORIGINS env)
"""

import os
from pathlib import Path

# Directorio base del proyecto
BASE_DIR = Path(__file__).parent.parent


class Config:
    """
    Configuración base común a todos los ambientes.
    
    RESPONSABILIDAD (1):
      1️⃣  Proporcionar valores base compartidos entre development/testing/production
    
    Estos valores pueden ser overrideados por subclases específicas del ambiente.
    Todos los valores son sensibles a variables de entorno.
    """
    
    # 🔐 Seguridad
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'False') == 'True'
    TESTING = False
    
    # 🗄️  Base de datos
    DATABASE_PATH = os.getenv('DB_PATH', BASE_DIR / 'control_existencias.db')
    DATABASE_URL = f'sqlite:///{DATABASE_PATH}'
    
    # 📡 API Flask
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = True
    
    # 🌐 CORS
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:5000').split(',')
