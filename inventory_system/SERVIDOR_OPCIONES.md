# Opciones para Ejecutar el Servidor de Forma Estable

## 📋 Resumen de Opciones

| Opción | Facilidad | Estabilidad | Requisitos | Reintentos |
|--------|-----------|-------------|-----------|-----------|
| **Script PowerShell** | ⭐ Muy fácil | ⭐ Media | Nada extra | Infinitos |
| **Gunicorn** | ⭐⭐ Media | ⭐⭐⭐ Alta | `pip install gunicorn` | Automáticos |
| **NSSM (Servicio)** | ⭐⭐⭐ Difícil | ⭐⭐⭐ Alta | Descargar NSSM | Automáticos |
| **Task Scheduler** | ⭐⭐ Media | ⭐⭐ Media | Windows nativo | Manual |
| **PM2** | ⭐⭐ Media | ⭐⭐⭐ Alta | Node.js | Automáticos |

---

## 🚀 OPCIÓN 1: Script PowerShell (RECOMENDADA PARA EMPEZAR)

### Ventajas:
- ✅ Sin requisitos adicionales
- ✅ Reintentos infinitos
- ✅ Logs en consola
- ✅ Fácil de usar

### Uso:
```powershell
# Navegar a la carpeta del proyecto
cd "c:\Users\luisr\OneDrive\Proyectos\Gestion de inventario\Code-Companion\inventory_system"

# Ejecutar el script
.\start_server.ps1
```

Si sale error de permisos:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Resultado:** Se reinsticia automáticamente cada vez que se cuelga.

---

## 🔧 OPCIÓN 2: Gunicorn (RECOMMENDED FOR PRODUCTION)

### Ventajas:
- ✅ Servidor WSGI profesional
- ✅ Múltiples workers = más robusto
- ✅ Mejor manejo de conexiones
- ✅ Logs detallados

### Instalación:
```bash
pip install gunicorn
```

### Uso:
```bash
cd "c:\Users\luisr\OneDrive\Proyectos\Gestion de inventario\Code-Companion\inventory_system"
python run_gunicorn.py
```

O directamente con Gunicorn:
```bash
gunicorn --workers 4 --bind 0.0.0.0:8000 app:app
```

**Acceso:** http://127.0.0.1:8000 (nota: puerto 8000, no 5000)

---

## 🪟 OPCIÓN 3: Servicio de Windows (NSSM)

### Ventajas:
- ✅ Se inicia automáticamente con Windows
- ✅ Se ejecuta siempre en segundo plano
- ✅ Reintentos automáticos
- ✅ Logs persistentes

### Instalación:

**Paso 1:** Descargar NSSM
```
https://nssm.cc/download
Extraer en: C:\NSSM
```

**Paso 2:** Ejecutar generador (PowerShell como ADMINISTRADOR)
```powershell
cd "c:\Users\luisr\OneDrive\Proyectos\Gestion de inventario\Code-Companion\inventory_system"
python create_windows_service.py
```

**Paso 3:** Crear servicio (copiar comando del script anterior en PowerShell como ADMIN)

**Paso 4:** Verificar que está corriendo
```powershell
C:\NSSM\nssm status InventarioWeb
```

### Comandos útiles:
```powershell
# Iniciar
C:\NSSM\nssm start InventarioWeb

# Detener
C:\NSSM\nssm stop InventarioWeb

# Reiniciar
C:\NSSM\nssm restart InventarioWeb

# Ver logs
Get-Content "c:\Users\luisr\OneDrive\Proyectos\Gestion de inventario\Code-Companion\inventory_system\service.log" -Tail 50

# Desinstalar
C:\NSSM\nssm remove InventarioWeb
```

---

## ⏰ OPCIÓN 4: Task Scheduler de Windows

### Ventajas:
- ✅ Windows nativo (sin descargas)
- ✅ Se inicia con Windows
- ✅ Fácil de ver/editar

### Configuración:

1. Presionar `Win + R` → escribir `taskschd.msc` → Enter
2. Click en "Crear tarea básica"
3. Nombre: `InventarioWeb`
4. Trigger: "Al iniciar el equipo"
5. Acción: "Ejecutar programa"
   - Programa: `C:\Users\luisr\.venv\Scripts\python.exe`
   - Argumentos: `run.py`
   - Directorio inicio: `C:\Users\luisr\OneDrive\Proyectos\Gestion de inventario\Code-Companion\inventory_system`
6. Marcar: "Ejecutar con permisos más altos" (si se requiere)

---

## 📦 OPCIÓN 5: PM2 (Si tienes Node.js)

### Instalación:
```bash
npm install -g pm2
```

### Crear archivo `ecosystem.config.js`:
```javascript
module.exports = {
  apps: [{
    name: 'inventario',
    script: 'run.py',
    interpreter: 'python',
    cwd: 'c:/Users/luisr/OneDrive/Proyectos/Gestion de inventario/Code-Companion/inventory_system',
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '1G',
    error_file: 'logs/error.log',
    out_file: 'logs/out.log',
    log_date_format: 'YYYY-MM-DD HH:mm:ss Z'
  }]
};
```

### Uso:
```bash
pm2 start ecosystem.config.js
pm2 save
pm2 startup
```

---

## ✅ Mi Recomendación

### Para desarrollo local:
👉 **OPCIÓN 1: Script PowerShell** 
- Ejecutas una vez y olvidas
- Se reinicia automáticamente si falla

### Para "siempre corriendo":
👉 **OPCIÓN 3: NSSM (Servicio Windows)**
- Se inicia con Windows
- Reintentos automáticos
- Ejecución en segundo plano

### Para máxima estabilidad:
👉 **OPCIÓN 2: Gunicorn**
- Mejor servidor WSGI
- Múltiples workers
- Cubridor entre desarrollo y producción

---

## 🧪 Test: Verificar que funciona

```powershell
# Una vez que el servidor está corriendo, prueba:
Invoke-WebRequest -Uri "http://127.0.0.1:5000/" -UseBasicParsing

# O con Gunicorn:
Invoke-WebRequest -Uri "http://127.0.0.1:8000/" -UseBasicParsing

# Resultado esperado: StatusCode 200 ✅
```

---

## 🆘 Solución de Problemas

### El script no ejecuta
```powershell
# Permitir ejecución de scripts
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Puerto ya en uso
```bash
# Encontrar qué proceso usa el puerto
netstat -ano | findstr :5000

# Matar el proceso (reemplazar PID)
taskkill /PID <PID> /F
```

### Ver logs del servicio
```powershell
Get-EventLog -LogName System -Source NSSM -Newest 10
```

---

## 📝 Conclusión

- **Empezar:** Usa el Script PowerShell
- **Producción:** Usa NSSM o Gunicorn
- **Máxima estabilidad:** Combina Gunicorn + NSSM
