# Script para instalar la tarea en Task Scheduler
# Ejecutar como ADMINISTRADOR

# Definir variables
$taskName = "InventarioWeb"
$xmlPath = "C:\Users\luisr\OneDrive\Proyectos\Gestion de inventario\Code-Companion\inventory_system\InventarioWeb_task.xml"
$projectPath = "C:\Users\luisr\OneDrive\Proyectos\Gestion de inventario\Code-Companion\inventory_system"

Write-Host "========================================" -ForegroundColor Green
Write-Host "Instalador de Tarea - Inventario Web" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Verificar si está ejecutando como admin
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "ERROR: Este script debe ejecutarse como ADMINISTRADOR" -ForegroundColor Red
    Write-Host ""
    Write-Host "Haz click derecho en instalar_tarea.bat y selecciona:" -ForegroundColor Yellow
    Write-Host '"Ejecutar como administrador"' -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Presiona ENTER para salir"
    exit 1
}

Write-Host "✅ Permisos de administrador detectados" -ForegroundColor Green
Write-Host ""

# Eliminar tarea anterior si existe
Write-Host "🔧 Eliminando tarea anterior si existe..."
try {
    $task = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
    if ($null -ne $task) {
        Write-Host "⚠️  Tarea existente encontrada. Eliminándola..."
        Unregister-ScheduledTask -TaskName $taskName -Confirm:$false | Out-Null
        Start-Sleep -Seconds 1
        Write-Host "✅ Tarea anterior eliminada"
    }
}
catch {
    Write-Host "ℹ️  Ninguna tarea anterior detectada" -ForegroundColor Cyan
}

Write-Host ""

# Crear nueva tarea desde XML
Write-Host "📋 Registrando nueva tarea..."
try {
    [xml]$xmlContent = Get-Content -Path $xmlPath -Encoding UTF16
    $taskXml = $xmlContent.OuterXml
    Register-ScheduledTask -Xml $taskXml -TaskName $taskName -Force | Out-Null
    Write-Host "✅ Tarea registrada correctamente" -ForegroundColor Green
}
catch {
    Write-Host "ERROR al registrar tarea: $_" -ForegroundColor Red
    Read-Host "Presiona ENTER para salir"
    exit 1
}

Write-Host ""

# Iniciar tarea
Write-Host "▶️  Iniciando tarea..."
try {
    Start-ScheduledTask -TaskName $taskName
    Start-Sleep -Seconds 2
    Write-Host "✅ Tarea iniciada" -ForegroundColor Green
}
catch {
    Write-Host "⚠️  Error al iniciar: $_" -ForegroundColor Yellow
}

Write-Host ""

# Verificar estado
Write-Host "📊 Verificando estado..."
try {
    $task = Get-ScheduledTask -TaskName $taskName
    $info = Get-ScheduledTaskInfo -TaskName $taskName
    $state = $task.State
    $lastRun = $info.LastRunTime
    $lastResult = $info.LastTaskResult
    
    Write-Host "   Estado: $state" -ForegroundColor Cyan
    Write-Host "   Última ejecución: $lastRun" -ForegroundColor Cyan
    Write-Host "   Último resultado: $lastResult" -ForegroundColor Cyan
}
catch {
    Write-Host "⚠️  Error al verificar estado" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "INSTALACION COMPLETADA" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

Write-Host "La tarea ahora:" -ForegroundColor Cyan
Write-Host "  ✅ Se inicia automáticamente con Windows"
Write-Host "  ✅ Se reinicia si el servidor falla"
Write-Host "  ✅ Se ejecuta con permisos de SISTEMA"
Write-Host "  ✅ Accesible en http://127.0.0.1:5000"
Write-Host ""

Write-Host "Comandos útiles:" -ForegroundColor Yellow
Write-Host "  Ver estado:    Get-ScheduledTask -TaskName 'InventarioWeb'" -ForegroundColor Gray
Write-Host "  Iniciar:       Start-ScheduledTask -TaskName 'InventarioWeb'" -ForegroundColor Gray
Write-Host "  Detener:       Stop-ScheduledTask -TaskName 'InventarioWeb'" -ForegroundColor Gray
Write-Host "  Reiniciar:     Restart-ScheduledTask -TaskName 'InventarioWeb'" -ForegroundColor Gray
Write-Host "  Ver logs:      Get-ScheduledTaskInfo -TaskName 'InventarioWeb'" -ForegroundColor Gray
Write-Host ""

Read-Host "Presiona ENTER para cerrar"
