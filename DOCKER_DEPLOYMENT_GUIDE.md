# 🚀 Guía Completa: Dockerizar y Desplegar en la Nube

## 📋 Requisitos Previos
- Docker instalado (https://docs.docker.com/get-docker/)
- Docker Compose instalado (v2.0+)
- Cuenta en uno de los servicios cloud (AWS, Google Cloud, Azure, DigitalOcean)
- Git CLI
- Una variable `.env` configurada

---

## 🐳 OPCIÓN 1: Ejecutar Localmente con Docker

### 1.1 Construir las imágenes
```bash
cd "C:\Users\luisr\OneDrive\Proyectos\Gestion de inventario\Code-Companion"
docker-compose build
```

### 1.2 Iniciar los servicios
```bash
docker-compose up -d
```

### 1.3 Verificar que todo está corriendo
```bash
docker-compose ps
docker-compose logs -f
```

### 1.4 Acceder a la aplicación
- **Frontend**: http://localhost
- **API**: http://localhost:3000

### 1.5 Detener los servicios
```bash
docker-compose down
```

---

## 🌐 OPCIÓN 2: Deploying a Docker Hub

### 2.1 Crear cuenta en Docker Hub
- Visita: https://hub.docker.com/signup
- Crea una cuenta

### 2.2 Hacer login
```bash
docker login
# Ingresa tu usuario y contraseña
```

### 2.3 Construir imágenes con tags
```bash
docker build -t tusuario/inventario-api:latest -f artifacts/api-server/Dockerfile .
docker build -t tusuario/inventario-ui:latest -f artifacts/inventario-ui/Dockerfile .
```

### 2.4 Subir a Docker Hub
```bash
docker push tusuario/inventario-api:latest
docker push tusuario/inventario-ui:latest
```

### 2.5 Verificar en Docker Hub
- https://hub.docker.com/repositories

---

## ☁️ OPCIÓN 3: AWS (Recomendado para Producción)

### 3.1 Configurar AWS CLI
```bash
# Instalar: https://aws.amazon.com/cli/
aws configure
# Ingresa: Access Key ID, Secret Access Key, Region (ej: us-east-1)
```

### 3.2 Crear ECR Repository
```bash
# Para API
aws ecr create-repository --repository-name inventario-api --region us-east-1

# Para UI
aws ecr create-repository --repository-name inventario-ui --region us-east-1
```

### 3.3 Obtener token de login
```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin {ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com
```

### 3.4 Construir y subir imágenes
```bash
# API
docker build -t {ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/inventario-api:latest -f artifacts/api-server/Dockerfile .
docker push {ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/inventario-api:latest

# UI
docker build -t {ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/inventario-ui:latest -f artifacts/inventario-ui/Dockerfile .
docker push {ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/inventario-ui:latest
```

### 3.5 Desplegar con ECS (Elastic Container Service)
1. Ve a AWS Console → ECS
2. Crea un nuevo cluster
3. Crea una task definition con ambas imágenes
4. Crea un servicio y desplegamientos

**Alternativa más sencilla: usar AWS App Runner**
1. Ve a App Runner en AWS Console
2. Conecta tu repositorio GitHub
3. Selecciona la rama y el Dockerfile
4. AWS desplegará automáticamente

---

## 🔷 OPCIÓN 4: Google Cloud (App Engine o Cloud Run)

### 4.1 Instalar Google Cloud CLI
```bash
# https://cloud.google.com/sdk/docs/install
gcloud init
```

### 4.2 Configurar proyecto
```bash
gcloud config set project tu-proyecto-id
```

### 4.3 Desplegar con Cloud Run (La más sencilla)

**Para la API:**
```bash
gcloud run deploy inventario-api \
  --source . \
  --dockerfile artifacts/api-server/Dockerfile \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

**Para la UI:**
```bash
gcloud run deploy inventario-ui \
  --source . \
  --dockerfile artifacts/inventario-ui/Dockerfile \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### 4.4 Obtener URLs de tu aplicación
```bash
gcloud run services list
```

---

## 🟦 OPCIÓN 5: Azure (Recomendado)

### 5.1 Instalar Azure CLI
```bash
# https://docs.microsoft.com/en-us/cli/azure/install-azure-cli
az login
```

### 5.2 Crear un contenedor registry
```bash
az group create --name mi-grupo --location eastus
az acr create --resource-group mi-grupo --name miregistro --sku Basic
```

### 5.3 Buildear y subir
```bash
az acr build --registry miregistro --image inventario-api:latest -f artifacts/api-server/Dockerfile .
az acr build --registry miregistro --image inventario-ui:latest -f artifacts/inventario-ui/Dockerfile .
```

### 5.4 Desplegar con Azure Container Instances
```bash
az container create \
  --resource-group mi-grupo \
  --name inventario-api \
  --image miregistro.azurecr.io/inventario-api:latest \
  --ports 3000 \
  --environment-variables NODE_ENV=production
```

---

## 💧 OPCIÓN 6: DigitalOcean (La más barata y amigable)

### 6.1 Crear una cuenta
- https://www.digitalocean.com/

### 6.2 Instalar doctl (CLI de DigitalOcean)
```bash
# https://docs.digitalocean.com/reference/doctl/how-to/install/
doctl auth init
```

### 6.3 Crear un Droplet (VPS)
```bash
# Opción fácil: Ve a DigitalOcean Console y crea un Droplet
# Elige: Docker Image (Ubuntu 22.04 with Docker)
# Elige el plan más barato ($4-6/mes)
```

### 6.4 Conectarte al servidor
```bash
ssh root@tu-ip-del-servidor
```

### 6.5 Clonar tu repositorio
```bash
git clone https://github.com/luisrendcn/Gestor-de-Inventario.git
cd Gestor-de-Inventario/Code-Companion
```

### 6.6 Crear archivo .env en el servidor
```bash
nano .env
# Agrega tus variables (DATABASE_URL, etc.)
```

### 6.7 Iniciar con Docker Compose
```bash
docker-compose up -d
```

### 6.8 Configurar dominio (opcional)
```bash
# Punto tu dominio a la IP del servidor
# Usa Let's Encrypt/Certbot para SSL
```

---

## 📊 Tabla Comparativa

| Plataforma    | Costo      | Dificultad | Escalado | Mejor Para                  |
|---------------|-----------|-----------|----------|----------------------------|
| Docker Hub    | Gratis    | Fácil     | Manual   | Almacenar imágenes          |
| AWS          | Variable   | Media     | Automático | Producción empresarial      |
| Google Cloud  | Variable   | Fácil     | Automático | Startups, rápido           |
| Azure        | Variable   | Media     | Automático | Integraciones Microsoft     |
| DigitalOcean | $6-12/mes | Fácil     | Manual   | Proyectos pequeños          |

---

## 🔒 Mejores Prácticas de Seguridad

### 1. Usar secrets management
```bash
# No incluyas .env en git
echo ".env" >> .gitignore
git rm --cached .env
```

### 2. Usar variables de entorno en producción
- AWS Secrets Manager
- Google Cloud Secret Manager
- Azure Key Vault
- DigitalOcean App Platform

### 3. Ejemplo: DigitalOcean App Platform (Más automático)
```bash
# Crea un archivo app.yaml
```

---

## 🧪 Testing Antes de Desplegar

```bash
# 1. Construir localmente
docker-compose build

# 2. Verificar que los servicios inician
docker-compose up -d

# 3. Probar los endpoints
curl http://localhost:3000/health
curl http://localhost

# 4. Ver logs
docker-compose logs -f

# 5. Detener
docker-compose down
```

---

## 📈 Monitoreo en Producción

### AWS
- CloudWatch para logs
- Auto Scaling para escalar según demanda

### Google Cloud
- Cloud Logging
- Cloud Monitoring

### Azure
- Application Insights
- Azure Monitor

### DigitalOcean
- Built-in monitoring
- Uptime monitoring

---

## 🚨 Solución de Problemas

### Problema: "port already in use"
```bash
# Cambiar puerto en docker-compose.yml
# Ej: "8080:80" en lugar de "80:80"
```

### Problema: "Connection refused" entre contenedores
```bash
# Asegúrate de que los servicios estén en la misma red
# Verifica docker-compose.yml tiene "networks"
```

### Problema: Imágenes muy grandes
```bash
# Usa multi-stage builds (ya incluido en los Dockerfiles)
# Limpia caché: docker builder prune
```

---

## ✅ Checklist Final

- [ ] Tengo `.env` configurado localmente
- [ ] Docker & Docker Compose instalados
- [ ] `docker-compose up -d` funciona
- [ ] Puedo acceder a http://localhost
- [ ] Imágenes construidas sin errores
- [ ] He hecho push a un registro (Docker Hub, AWS ECR, etc.)
- [ ] He probado el deployment en la nube
- [ ] La aplicación es accesible desde internet
- [ ] He configurado dominio (opcional)
- [ ] He configurado SSL/HTTPS (recomendado)

---

## 📞 Próximos Pasos

1. **Elige tu plataforma** según tu presupuesto y necesidades
2. **Sigue los pasos** específicos de esa plataforma
3. **Prueba localmente primero** con `docker-compose up`
4. **Monitoreа en producción** según los servicios que ofrece tu plataforma
5. **Configura CI/CD** (GitHub Actions, GitLab CI) para deploys automáticos

¡Listo! Tu aplicación estará disponible en la nube 🎉
