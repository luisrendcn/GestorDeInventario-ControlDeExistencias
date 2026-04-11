@echo off
setlocal enabledelayedexpansion

echo.
echo ========================================
echo Creando servicio de Windows...
echo ========================================
echo.

echo Paso 1: Instalando servicio...
C:\NSSM\nssm install InventarioWeb "C:\Users\luisr\AppData\Local\Python\pythoncore-3.14-64\python.exe" "C:\Users\luisr\OneDrive\Proyectos\Gestion de inventario\Code-Companion\inventory_system\service_wrapper.py"

echo Paso 2: Configurando directorio...
C:\NSSM\nssm set InventarioWeb AppDirectory "C:\Users\luisr\OneDrive\Proyectos\Gestion de inventario\Code-Companion\inventory_system"

echo Paso 3: Configurando logs...
C:\NSSM\nssm set InventarioWeb AppStdout "C:\Users\luisr\OneDrive\Proyectos\Gestion de inventario\Code-Companion\inventory_system\service.log"
C:\NSSM\nssm set InventarioWeb AppStderr "C:\Users\luisr\OneDrive\Proyectos\Gestion de inventario\Code-Companion\inventory_system\service_error.log"

echo Paso 4: Iniciando servicio...
C:\NSSM\nssm start InventarioWeb

echo.
echo ========================================
echo ✅ Servicio creado exitosamente
echo ========================================
echo.
echo El servidor se inicia automáticamente con Windows
echo Acceso: http://127.0.0.1:5000
echo.
pause
