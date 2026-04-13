#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
╔════════════════════════════════════════════════════════════════════════════╗
║                  ARCHIVO: run.py                                          ║
║                  FUNCIÓN: Launcher/Punto de entrada                       ║
╚════════════════════════════════════════════════════════════════════════════╝

📋 RESPONSABILIDAD DEL ARCHIVO:
   Script para iniciar la aplicación Flask con verificaciones previas
   antes de ejecutar el servidor.

🎯 FUNCIONALIDADES:
   ✓ Verificar dependencias instaladas (Flask, dotenv)
   ✓ Verificar archivo .env (opcional)
   ✓ Verificar conexión a base de datos
   ✓ Iniciar la aplicación Flask

⚙️ EJECUCIÓN:
   python run.py
   o
   flask run (si está configurado)

📍 FUNCIONES DISPONIBLES:
   • verificar_dependencias() → Valida que Flask y dotenv estén instalados
   • verificar_env() → Valida que exista .env (opcional para SQLite)
   • verificar_db() → Prueba conexión a base de datos
"""

import os
import sys
from pathlib import Path

# Cambiar al directorio del script
os.chdir(str(Path(__file__).parent))

# Agregar directorio actual al path
sys.path.insert(0, str(Path(__file__).parent))

def verificar_dependencias():
    """Verifica que todas las dependencias estén instaladas"""
    dependencias = ['flask', 'dotenv']
    faltantes = []
    
    for modulo in dependencias:
        try:
            if modulo == 'flask':
                import flask
            elif modulo == 'dotenv':
                import dotenv
        except ImportError:
            faltantes.append(modulo)
    
    if faltantes:
        print("❌ Dependencias faltantes:", ', '.join(faltantes))
        print("\n📦 Instalar con:")
        print("   pip install -r requirements.txt")
        return False
    
    return True

def verificar_env():
    """Verifica que exista archivo .env (opcional para SQLite)"""
    return True  # No requerido para SQLite

def verificar_db():
    """Verifica que SQLite esté disponible (sin tocar la BD real)"""
    try:
        import sqlite3
        # Usar base de datos en memoria para verificar que SQLite funciona
        # sin interferir con los archivos WAL/SHM de la base de datos real
        temp_conn = sqlite3.connect(":memory:")
        temp_conn.close()
        print("✅ Base de datos: SQLite disponible")
        return True
    except Exception as e:
        print(f"❌ Error de conexión a BD: {e}")
        print("\n📋 La base de datos SQLite se crea automáticamente")
        print("   Si persiste el error, verifica que SQLite esté instalado")
        return False

def main():
    """Función principal"""
    print("\n" + "="*60)
    print("🚀 CONTROL DE EXISTENCIAS - Sistema de Inventario")
    print("="*60 + "\n")
    
    # Verificaciones
    print("📋 Verificando requisitos...")
    
    if not verificar_dependencias():
        sys.exit(1)
    print("✅ Dependencias: OK")
    
    if not verificar_env():
        sys.exit(1)
    print("✅ Configuración: OK")
    
    if not verificar_db():
        print("\n💡 Tip: Verifica que el directorio sea escribible")
        print("   La BD SQLite se crea automáticamente en: control_existencias.db")
        sys.exit(1)
    
    print("\n" + "="*60)
    print("✨ Iniciando servidor Flask...")
    print("="*60)
    print("\n🌐 Abrir navegador en: http://localhost:5000")
    print("📊 API disponible en: http://localhost:5000/api")
    print("🛑 Presiona Ctrl+C para detener\n")
    
    # Importar y ejecutar Flask
    from app import app
    
    try:
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=False,
            use_reloader=False
        )
    except KeyboardInterrupt:
        print("\n\n👋 Servidor detenido")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error al iniciar: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
