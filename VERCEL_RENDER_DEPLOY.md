# 🚀 Deploy Rápido: Vercel + Render (5 minutos)

## **FRONTEND: Vercel (La Parte Fácil) ⭐**

### 1️⃣ Instalar Vercel CLI
```bash
npm install -g vercel
```

### 2️⃣ Login
```bash
vercel login
# Selecciona GitHub
```

### 3️⃣ Deploy
```bash
cd artifacts/inventario-ui
vercel
```

**Responde el wizard:**
- Project name: `inventario-ui` (Enter)
- Framework: Autodetectado (Enter)
- Root directory: `./` (Enter)
- Build command: `npm run build` (Enter)
- Output directory: `dist` (Enter)

**RESULTADO:** Tu Frontend en `https://inventario-ui.vercel.app`

---

## **BACKEND: Render (Rápido y Gratis) ⚡**

### 1️⃣ Ir a Render
- https://render.com

### 2️⃣ Sign Up con GitHub
- Clic en "Sign up with GitHub"
- Autoriza la app

### 3️⃣ Crear Web Service
- Clic en "New +"
- Selecciona "Web Service"
- Autoriza acceso a tu repositorio GitHub

### 4️⃣ Configurar
```
Name: inventario-api
Root Directory: Code-Companion/artifacts/api-server
Build Command: npm run build
Start Command: npm run start
```

### 5️⃣ Environment Variables
- Si tu `.env` tiene variables, cópialas aquí
- Ejemplo: `NODE_ENV=production`

### 6️⃣ Deploy
- Clic en "Create Web Service"
- Espera ~3-5 minutos
- **RESULTADO:** Tu Backend en `https://inventario-api.onrender.com`

---

## **🔗 CONECTAR FRONTEND Y BACKEND**

### En Vercel (Frontend):
1. Ir a https://vercel.com/dashboard
2. Selecciona tu proyecto `inventario-ui`
3. Settings → Environment Variables
4. Agrega:
   ```
   VITE_API_URL=https://inventario-api.onrender.com
   ```
5. Redeploy

**O Más Fácil:** 
Editar [.env.production](.env.production):
```bash
VITE_API_URL=https://inventario-api.onrender.com
```
Y hacer push a GitHub. Vercel redesplegará automáticamente.

---

## ✅ **Verificar que funciona**

1. Abre `https://inventario-ui.vercel.app`
2. Si ves datos, ¡todo está funcionando! ✅
3. Si no, verifica:
   - API está corriendo: `https://inventario-api.onrender.com/health`
   - VITE_API_URL está correcto

---

## 📊 **Resumen de Costos**

| Servicio | Costo | Límites |
|----------|-------|---------|
| **Vercel Frontend** | Gratis | 100 GB bandwith/mes |
| **Render Backend** | Gratis | Ilimitado |
| **TOTAL** | **Gratis** | **Sin límites reales** |

---

## 🔄 **Flujo de Updates**

Ahora solo necesitas:

```bash
# 1. Hacer cambios locales
# 2. Commit y push
git add .
git commit -m "tu mensaje"
git push origin main

# 3. Vercel y Render se actualizan automáticamente
# 4. Espera 2-3 minutos
# 5. Tu app está actualizada en la nube
```

**NO necesitas hacer nada más. Automático.** ✅

---

## 🎯 **URLs Finales**

- **Frontend:** https://inventario-ui.vercel.app
- **Backend:** https://inventario-api.onrender.com
- **GitHub:** https://github.com/luisrendcn/Gestor-de-Inventario

---

## ⚡ **BONUS: Si quieres un dominio personalizado**

**Opción 1: Vercel (Cambia el dominio)**
1. Ir a Vercel Dashboard → inventario-ui
2. Settings → Domains
3. Agrega tu dominio: `tudominio.com`

**Opción 2: Render (Agregar a tu dominio)**
1. Ir a Render Dashboard → inventario-api
2. Settings → Custom Domain
3. Configura DNS

---

## 🆘 **Problemas Comunes**

### Error "Cannot find module"
```bash
# En Render, agrega:
npm install
npm run build
```

### "403 Forbidden" al llamar la API
- Verifica CORS en tu backend
- API debe estar públicamente accesible

### Render se duerme (free tier)
- Se reinicia después de 15 min inactividad
- Primer reinicio tarda 30 segundos
- **Solución:** Cambiar a Fly.io (siempre activo gratis)

---

## 🚀 **Listo!**

Con esto tienes:
- ✅ Frontend en Vercel
- ✅ Backend en Render  
- ✅ Deploy automático con cada push
- ✅ HTTPS en ambos
- ✅ Completamente gratis

**Tiempo total: ~10 minutos** ⏱️
