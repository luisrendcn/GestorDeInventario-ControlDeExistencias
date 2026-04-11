@echo off
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
powershell -ExecutionPolicy Bypass -File "C:\Users\luisr\OneDrive\Proyectos\Gestion de inventario\Code-Companion\inventory_system\instalar_tarea.ps1"

pause
