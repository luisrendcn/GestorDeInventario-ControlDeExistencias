@echo off
REM Instalador de Tarea - Inventario Web
REM Requiere permisos de ADMINISTRADOR

setlocal enabledelayedexpansion

echo.
echo ========================================
echo Instalador de Tarea - Inventario Web
echo ========================================
echo.

REM Verificar si es administrador
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: Este script debe ejecutarse como ADMINISTRADOR
    echo.
    echo Haz click derecho en este archivo y selecciona:
    echo "Ejecutar como administrador"
    echo.
    pause
    exit /b 1
)

echo OK Permisos de administrador detectados
echo.

REM Definir variables
set TASK_NAME=InventarioWeb
set SCRIPT_PATH=%~dp0service_wrapper.py
set PYTHON_EXE=C:\Users\luisr\AppData\Local\Python\pythoncore-3.14-64\python.exe

REM Verificar que Python existe
if not exist "%PYTHON_EXE%" (
    echo ERROR: Python no encontrado en %PYTHON_EXE%
    echo.
    pause
    exit /b 1
)

echo Eliminando tarea anterior si existe...
schtasks /delete /tn %TASK_NAME% /f 2>nul
if %errorLevel% equ 0 (
    echo OK Tarea anterior eliminada
) else (
    echo INFO Ninguna tarea anterior detectada
)

echo.
echo Creando nueva tarea...

REM Crear tarea que se ejecuta al iniciar o al conectarse
schtasks /create /tn %TASK_NAME% /tr "cmd /c cd /d %~dp0 && %PYTHON_EXE% service_wrapper.py" /sc onstart /ru SYSTEM /f

if %errorLevel% neq 0 (
    echo ERROR: No se pudo crear la tarea
    pause
    exit /b 1
)

echo OK Tarea creada exitosamente
echo.

REM Inicia la tarea inmediatamente
echo Iniciando tarea...
schtasks /run /tn %TASK_NAME%

if %errorLevel% neq 0 (
    echo ADVERTENCIA: Error al iniciar manualmente, pero la tarea esta programada
) else (
    echo OK Tarea iniciada
)

echo.
echo Verificando estado...
schtasks /query /tn %TASK_NAME% /v /fo list

echo.
echo ========================================
echo INSTALACION COMPLETADA
echo ========================================
echo.

echo La tarea ahora:
echo   OK Se inicia automaticamente con Windows
echo   OK Se reinicia si el servidor falla
echo   OK Se ejecuta con permisos de SISTEMA
echo   OK Accesible en http://127.0.0.1:5000
echo.

echo Comandos utiles:
echo   Ver estado:  schtasks /query /tn InventarioWeb
echo   Iniciar:     schtasks /run /tn InventarioWeb
echo   Detener:     taskkill /f /im python.exe
echo   Ver logs:    Get-ScheduledTaskInfo -TaskName InventarioWeb
echo.

pause
