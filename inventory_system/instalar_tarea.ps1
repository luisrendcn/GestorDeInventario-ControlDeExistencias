# Script para instalar la tarea en Task Scheduler
# Ejecutar como ADMINISTRADOR

# Definir variables
$taskName = "InventarioWeb"
$xmlPath = "C:\Users\luisr\OneDrive\Proyectos\Gestion de inventario\Code-Companion\inventory_system\InventarioWeb_task.xml"
$taskPath = "\InventarioWeb"

Write-Host "🔧 Instalando tarea en Task Scheduler..."

# Eliminar tarea anterior si existe
try {
    $task = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
    if ($null -ne $task) {
        Write-Host "⚠️  Tarea existente encontrada. Eliminándola..."
        Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
        Start-Sleep -Seconds 1
    }
} catch {
    Write-Host "ℹ️  Ninguna tarea anterior detectada"
}

# Crear nueva tarea desde XML
try {
    Write-Host "📋 Registrando nueva tarea..."
    Register-ScheduledTask -Xml (Get-Content $xmlPath | Out-String) -TaskName $taskName -Force | Out-Null
    Write-Host "✅ Tarea registrada correctamente"
} catch {
    Write-Host "❌ Error al registrar tarea: $_"
    exit 1
}

# Iniciar tarea
try {
    Write-Host "▶️  Iniciando tarea..."
    Start-ScheduledTask -TaskName $taskName
    Start-Sleep -Seconds 2
    Write-Host "✅ Tarea iniciada"
} catch {
    Write-Host "⚠️  Error al iniciar: $_"
}

# Verificar estado
try {
    $task = Get-ScheduledTask -TaskName $taskName
    $lastRun = $task.LastRunTime
    $state = $task.State
    Write-Host "📊 Estado actual:"
    Write-Host "   Estado: $state"
    Write-Host "   Última ejecución: $lastRun"
} catch {
    Write-Host "⚠️  Error al verificar estado"
}

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
Write-Host "  Ver estado:    Get-ScheduledTask -TaskName 'InventarioWeb'"
Write-Host "  Iniciar:       Start-ScheduledTask -TaskName 'InventarioWeb'"
Write-Host "  Detener:       Stop-ScheduledTask -TaskName 'InventarioWeb'"
Write-Host "  Reiniciar:     Restart-ScheduledTask -TaskName 'InventarioWeb'"
Write-Host "  Ver logs:      Get-ScheduledTaskInfo -TaskName 'InventarioWeb'"
Write-Host ""
