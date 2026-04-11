# 📦 Sistema de Gestión de Inventario

## Control de Existencias

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Crear base de datos
createdb control_existencias

# 3. Ejecutar
python run.py

# Abrir navegador: http://localhost:5000
```

## 📊 Interfaz web

- **Dashboard**: Estadísticas y alertas en vivo
- **Productos**: CRUD (crear, leer, actualizar, eliminar)
- **Operaciones**: Entrada/salida/ajuste de stock
- **Reportes**: Estadísticas generales
- **Historial**: Auditoría de movimientos

## 🔌 API REST (11 endpoints)

Todos disponibles en `http://localhost:5000/api/`

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | /api/productos | Listar todos |
| POST | /api/productos | Crear |
| DELETE | /api/productos/{id} | Eliminar |
| POST | /api/entrada | Entrada de stock |
| POST | /api/salida | Salida de stock |
| POST | /api/ajuste | Ajuste por auditoría |
| GET | /api/reporte | Estadísticas |
| GET | /api/alertas | Stock bajo/agotado |
| GET | /api/historial | Movimientos |

## 🐛 Problemas comunes

**Error: "Could not connect to database"**
```bash
# Verificar PostgreSQL está corriendo
# Crear la base de datos:
createdb control_existencias

# Revisar .env con credenciales correctas
```

**Error: "ModuleNotFoundError: No module named 'flask'"**
```bash
pip install -r requirements.txt
```

**Puerto 5000 ya en uso**
```
Editar app.py línea ~200:
app.run(port=5001)  # Cambiar a otro puerto
```

## 🎯 Flujo típico

1. Crear productos (Dashboard → Productos → Crear)
2. Registrar entrada (Operaciones → Entrada)
3. Registrar salida (Operaciones → Salida)
4. Ver reporte (Reportes)
5. Consultar historial (Historial)

Stack: Flask + SQLite + HTML/CSS/JS
