"""
create_windows_service.py
==========================
Crea un servicio de Windows que ejecuta el servidor automáticamente.

El servicio se inicia con Windows y se reinicia si falla.
"""

import os
import sys
import subprocess
from pathlib import Path

def crear_servicio():
    """Crea el servicio de Windows"""
    
    # Rutas
    python_exe = sys.executable
    project_path = Path(__file__).parent
    run_py = project_path / "run.py"
    
    # Nombre del servicio
    service_name = "InventarioWeb"
    display_name = "Sistema de Control de Existencias"
    
    print("🔧 Creando servicio de Windows...")
    print(f"   Nombre: {service_name}")
    print(f"   Display: {display_name}")
    print(f"   Python: {python_exe}")
    print(f"   Script: {run_py}\n")
    
    # Crear script wrapper que hace reintentos
    wrapper_script = project_path / "service_wrapper.py"
    wrapper_content = f'''#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import time
import subprocess

os.chdir(r"{project_path}")

max_retries = 0  # Reintentos infinitos
retry_count = 0

while True:
    try:
        print(f"[{{time.strftime('%Y-%m-%d %H:%M:%S')}}] Iniciando servidor...")
        result = subprocess.run([r"{python_exe}", "run.py"], check=False)
        
        if result.returncode != 0:
            retry_count += 1
            print(f"[{{time.strftime('%Y-%m-%d %H:%M:%S')}}] ❌ Servidor falló (reintento {{retry_count}})")
            time.sleep(5)  # Esperar 5 segundos antes de reintentar
        else:
            break
    except KeyboardInterrupt:
        print("\\n[{{time.strftime('%Y-%m-%d %H:%M:%S')}}] Servicio detenido")
        break
    except Exception as e:
        retry_count += 1
        print(f"[{{time.strftime('%Y-%m-%d %H:%M:%S')}}] ❌ Error: {{e}}")
        time.sleep(5)
'''
    
    with open(wrapper_script, 'w', encoding='utf-8') as f:
        f.write(wrapper_content)
    
    print(f"✅ Wrapper creado: {wrapper_script}\n")
    
    # Comando para crear el servicio con NSSM
    print("📋 Instrucciones para crear el servicio:\n")
    
    print("PASO 1: Descargar NSSM")
    print("-" * 60)
    print("Descargar desde: https://nssm.cc/download")
    print("Extraer en: C:\\NSSM\n")
    
    print("PASO 2: Crear el servicio (PowerShell como ADMINISTRADOR)")
    print("-" * 60)
    print("Copiar y pegar estos comandos:\n")
    
    commands = f'''
# 1. Crear el servicio
C:\\NSSM\\nssm install {service_name} "{python_exe}" "{wrapper_script}"

# 2. Configurar directorio de trabajo
C:\\NSSM\\nssm set {service_name} AppDirectory "{project_path}"

# 3. Configurar archivos de log (opcional)
C:\\NSSM\\nssm set {service_name} AppStdout "{project_path}\\service.log"
C:\\NSSM\\nssm set {service_name} AppStderr "{project_path}\\service_error.log"

# 4. Iniciar el servicio
C:\\NSSM\\nssm start {service_name}

# 5. Verificar que está corriendo
C:\\NSSM\\nssm status {service_name}
    '''
    
    print(commands)
    
    print("\nPASO 3: Verificar que funciona")
    print("-" * 60)
    print("Abrir navegador en: http://127.0.0.1:5000")
    print("Debe mostrar la aplicación web\n")
    
    print("\nCOMMANDOS ÚTILES:")
    print("-" * 60)
    
    manage_commands = f'''
# Ver estado
C:\\NSSM\\nssm status {service_name}

# Iniciar
C:\\NSSM\\nssm start {service_name}

# Detener
C:\\NSSM\\nssm stop {service_name}

# Reiniciar
C:\\NSSM\\nssm restart {service_name}

# Ver logs
Get-Content "{project_path}\\service.log" -Tail 50

# Ver errores
Get-Content "{project_path}\\service_error.log" -Tail 50

# Desinstalar servicio (si es necesario)
C:\\NSSM\\nssm remove {service_name}

# Editar configuración
C:\\NSSM\\nssm edit {service_name}
    '''
    
    print(manage_commands)
    
    # Crear un script batch para facilitar
    batch_script = project_path / "crear_servicio.bat"
    batch_content = f'''@echo off
setlocal enabledelayedexpansion

echo.
echo ========================================
echo Creando servicio de Windows...
echo ========================================
echo.

echo Paso 1: Instalando servicio...
C:\\NSSM\\nssm install {service_name} "{python_exe}" "{wrapper_script}"

echo Paso 2: Configurando directorio...
C:\\NSSM\\nssm set {service_name} AppDirectory "{project_path}"

echo Paso 3: Configurando logs...
C:\\NSSM\\nssm set {service_name} AppStdout "{project_path}\\service.log"
C:\\NSSM\\nssm set {service_name} AppStderr "{project_path}\\service_error.log"

echo Paso 4: Iniciando servicio...
C:\\NSSM\\nssm start {service_name}

echo.
echo ========================================
echo ✅ Servicio creado exitosamente
echo ========================================
echo.
echo El servidor se inicia automáticamente con Windows
echo Acceso: http://127.0.0.1:5000
echo.
pause
'''
    
    with open(batch_script, 'w', encoding='utf-8') as f:
        f.write(batch_content)
    
    print(f"\n✅ Script batch creado: {batch_script}")
    print("   (Doble-click para ejecutar automáticamente)")
    
    return wrapper_script

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 INSTALADOR DE SERVICIO WINDOWS")
    print("   Sistema de Control de Existencias")
    print("="*60 + "\n")
    
    crear_servicio()
    
    print("\n" + "="*60)
    print("✅ Configuración lista")
    print("="*60)
    print("\nUna vez configurado, el servicio:")
    print("  ✅ Se inicia automáticamente con Windows")
    print("  ✅ Se reinicia si falla")
    print("  ✅ Se ejecuta en segundo plano")
    print("  ✅ Registra errores en logs")
    print("  ✅ Accesible en http://127.0.0.1:5000\n")
    
    print("IMPORTANTE:")
    print("  1. Descargar NSSM: https://nssm.cc/download")
    print("  2. Extraer en: C:\\NSSM")
    print("  3. Ejecutar los comandos en PowerShell como ADMINISTRADOR")
    print("  4. O doble-click en crear_servicio.bat (como ADMINISTRADOR)\n")
