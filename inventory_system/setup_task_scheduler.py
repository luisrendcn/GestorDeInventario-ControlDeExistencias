"""
setup_task_scheduler.py
=========================
Configura un servicio de Windows usando Task Scheduler (100% nativo).

NO requiere descargas externas como NSSM.
El servidor se inicia automáticamente con Windows y se reinicia si falla.
"""

import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime

def crear_task_scheduler():
    """Crea tarea automática en Task Scheduler"""
    
    # Rutas
    python_exe = sys.executable
    project_path = Path(__file__).parent.absolute()
    wrapper_script = project_path / "service_wrapper.py"
    
    # Nombre de la tarea
    task_name = "InventarioWeb"
    
    print("\n" + "="*70)
    print("🪟 CONFIGURADOR DE TASK SCHEDULER")
    print("   Sistema de Inventario - Ejecución Automática")
    print("="*70 + "\n")
    
    print("📋 Información de la tarea:")
    print(f"   Nombre: {task_name}")
    print(f"   Python: {python_exe}")
    print(f"   Script: {wrapper_script}")
    print(f"   Carpeta: {project_path}\n")
    
    # Crear archivo batch que ejecutará la tarea
    batch_script = project_path / "run_service.bat"
    batch_content = f'''@echo off
REM Ejecutar servidor con reintentos automáticos
cd /d "{project_path}"
:retry
echo [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Iniciando servidor...
python "{wrapper_script}"
echo [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Servidor detenido. Reintentando en 5 segundos...
timeout /t 5 /nobreak
goto retry
'''
    
    with open(batch_script, 'w', encoding='utf-8') as f:
        f.write(batch_content)
    
    print(f"✅ Script de ejecución creado: {batch_script}\n")
    
    # Crear archivo XML para la tarea
    task_xml = project_path / "InventarioWeb_task.xml"
    
    # Sanitizar rutas para XML
    batch_script_escaped = str(batch_script).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    
    xml_content = f'''<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.3" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Date>{datetime.now().isoformat()}</Date>
    <Author>InventarioWeb Setup</Author>
    <Description>Ejecuta el servidor de Control de Existencias automáticamente con reintentos</Description>
  </RegistrationInfo>
  <Triggers>
    <LogonTrigger>
      <Enabled>true</Enabled>
    </LogonTrigger>
    <BootTrigger>
      <Enabled>true</Enabled>
    </BootTrigger>
  </Triggers>
  <Principals>
    <Principal id="Author">
      <UserId>S-1-5-18</UserId>
      <RunLevel>HighestAvailable</RunLevel>
    </Principal>
  </Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <AllowHardTerminate>true</AllowHardTerminate>
    <StartWhenAvailable>true</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>
    <IdleSettings>
      <Duration>PT10M</Duration>
      <WaitTimeout>PT1H</WaitTimeout>
      <StopOnIdleEnd>false</StopOnIdleEnd>
      <RestartOnIdle>false</RestartOnIdle>
    </IdleSettings>
    <AllowStartOnDemand>true</AllowStartOnDemand>
    <Enabled>true</Enabled>
    <Hidden>false</Hidden>
    <RunOnlyIfIdle>false</RunOnlyIfIdle>
    <WakeToRun>true</WakeToRun>
    <ExecutionTimeLimit>PT0S</ExecutionTimeLimit>
    <Priority>7</Priority>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>{batch_script_escaped}</Command>
      <WorkingDirectory>{str(project_path).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")}</WorkingDirectory>
    </Exec>
  </Actions>
</Task>
'''
    
    with open(task_xml, 'w', encoding='utf-16') as f:
        f.write(xml_content)
    
    print(f"✅ Configuración XML creada: {task_xml}\n")
    
    # Crear script de instalación
    install_script = project_path / "instalar_tarea.ps1"
    install_content = f'''# Script para instalar la tarea en Task Scheduler
# Ejecutar como ADMINISTRADOR

# Definir variables
$taskName = "{task_name}"
$xmlPath = "{task_xml}"
$taskPath = "\\{task_name}"

Write-Host "🔧 Instalando tarea en Task Scheduler..."

# Eliminar tarea anterior si existe
try {{
    $task = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
    if ($null -ne $task) {{
        Write-Host "⚠️  Tarea existente encontrada. Eliminándola..."
        Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
        Start-Sleep -Seconds 1
    }}
}} catch {{
    Write-Host "ℹ️  Ninguna tarea anterior detectada"
}}

# Crear nueva tarea desde XML
try {{
    Write-Host "📋 Registrando nueva tarea..."
    Register-ScheduledTask -Xml (Get-Content $xmlPath | Out-String) -TaskName $taskName -Force | Out-Null
    Write-Host "✅ Tarea registrada correctamente"
}} catch {{
    Write-Host "❌ Error al registrar tarea: $_"
    exit 1
}}

# Iniciar tarea
try {{
    Write-Host "▶️  Iniciando tarea..."
    Start-ScheduledTask -TaskName $taskName
    Start-Sleep -Seconds 2
    Write-Host "✅ Tarea iniciada"
}} catch {{
    Write-Host "⚠️  Error al iniciar: $_"
}}

# Verificar estado
try {{
    $task = Get-ScheduledTask -TaskName $taskName
    $lastRun = $task.LastRunTime
    $state = $task.State
    Write-Host "📊 Estado actual:"
    Write-Host "   Estado: $state"
    Write-Host "   Última ejecución: $lastRun"
}} catch {{
    Write-Host "⚠️  Error al verificar estado"
}}

Write-Host ""
Write-Host "=========================================="
Write-Host "✅ Instalación completada"
Write-Host "=========================================="
Write-Host ""
Write-Host "La tarea ahora:"
Write-Host "  ✅ Se inicia automáticamente con Windows"
Write-Host "  ✅ Se reinicia si el servidor falla"
Write-Host "  ✅ Se ejecuta con permisos de SISTEMA"
Write-Host "  ✅ Accesible en http://127.0.0.1:5000"
Write-Host ""
Write-Host "Comandos útiles:"
Write-Host "  Ver estado:    Get-ScheduledTask -TaskName '{task_name}'"
Write-Host "  Iniciar:       Start-ScheduledTask -TaskName '{task_name}'"
Write-Host "  Detener:       Stop-ScheduledTask -TaskName '{task_name}'"
Write-Host "  Reiniciar:     Restart-ScheduledTask -TaskName '{task_name}'"
Write-Host "  Ver logs:      Get-ScheduledTaskInfo -TaskName '{task_name}'"
Write-Host ""
'''
    
    with open(install_script, 'w', encoding='utf-8') as f:
        f.write(install_content)
    
    print(f"✅ Script de instalación creado: {install_script}\n")
    
    # Crear script batch para ejecutar como admin
    install_batch = project_path / "instalar_tarea.bat"
    install_batch_content = f'''@echo off
echo ========================================
echo Instalador de Tarea - Inventario Web
echo ========================================
echo.
echo Este script requiere permisos de ADMINISTRADOR
echo.

REM Verificar si está ejecutando como admin
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ❌ ERROR: Este script debe ejecutarse como ADMINISTRADOR
    echo.
    echo Haz click derecho en este archivo y selecciona:
    echo "Ejecutar como administrador"
    echo.
    pause
    exit /b 1
)

echo ✅ Permisos de administrador detectados
echo.
echo Ejecutando instalación...
powershell -ExecutionPolicy Bypass -File "{install_script}"

pause
'''
    
    with open(install_batch, 'w', encoding='utf-8') as f:
        f.write(install_batch_content)
    
    print(f"✅ Script batch creado: {install_batch}\n")
    
    # Mostrar instrucciones
    print("="*70)
    print("📋 INSTRUCCIONES DE INSTALACIÓN")
    print("="*70 + "\n")
    
    print("OPCIÓN 1: Instalación automática (RECOMENDADO)")
    print("-" * 70)
    print(f"1. Hacer click derecho en: {install_batch}")
    print("2. Seleccionar: 'Ejecutar como administrador'")
    print("3. Presionar ENTER cuando termine\n")
    
    print("OPCIÓN 2: Instalación manual en PowerShell")
    print("-" * 70)
    print("1. Abrir PowerShell como ADMINISTRADOR")
    print(f"2. Ejecutar: powershell -ExecutionPolicy Bypass -File \"{install_script}\"\n")
    
    print("OPCIÓN 3: Instalación desde Task Scheduler GUI")
    print("-" * 70)
    print("1. Presionar Win+R")
    print("2. Escribir: taskschd.msc")
    print("3. Ir a: Acciones > Importar tarea")
    print(f"4. Seleccionar: {task_xml}\n")
    
    print("="*70)
    print("✅ CONFIGURACIÓN LISTA")
    print("="*70 + "\n")
    
    print("Una vez instalado, la tarea:")
    print("  ✅ Se inicia automáticamente con Windows")
    print("  ✅ Se reinicia si el servidor falla")
    print("  ✅ Se ejecuta con permisos de SISTEMA")
    print("  ✅ Accesible en http://127.0.0.1:5000")
    print("  ✅ Registra mensajes en el Event Viewer\n")
    
    print("Ver logs en:")
    print("  • Event Viewer > Windows Logs > System")
    print(f"  • Archivo: {project_path / 'service.log'}\n")
    
    return install_batch, install_script

if __name__ == '__main__':
    install_batch, install_script = crear_task_scheduler()
    
    print("="*70)
    print("🎯 PRÓXIMO PASO:")
    print("="*70)
    print(f"\nMake click derecho aquí → Ejecutar como administrador:")
    print(f"  {install_batch}\n")
