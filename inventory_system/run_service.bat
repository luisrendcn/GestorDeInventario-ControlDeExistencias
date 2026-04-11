@echo off
REM Ejecutar servidor con reintentos automáticos
cd /d "C:\Users\luisr\OneDrive\Proyectos\Gestion de inventario\Code-Companion\inventory_system"
:retry
echo [2026-04-10 20:40:36] Iniciando servidor...
python "C:\Users\luisr\OneDrive\Proyectos\Gestion de inventario\Code-Companion\inventory_system\service_wrapper.py"
echo [2026-04-10 20:40:36] Servidor detenido. Reintentando en 5 segundos...
timeout /t 5 /nobreak
goto retry
