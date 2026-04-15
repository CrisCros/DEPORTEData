# Guía CI/CD — Backend DEPORTEData

Guía paso a paso para cuando alguien modifica el backend: desde el commit hasta el despliegue en EC2.

---

## Flujo completo

```
feat/mi-cambio → develop → main → tag → GitHub Actions → GHCR → EC2
```

---

## Paso 1 — Crear rama y hacer cambios

Desde la rama `develop`, crea una rama de feature:

```bash
git checkout develop
git pull origin develop
git checkout -b feat/mi-cambio
```

Haz tus cambios en `backend/` y commitea con Conventional Commits:

```bash
git add backend/
git commit -m "feat(backend): añadir endpoint de forecast"
git push origin feat/mi-cambio
```

---

## Paso 2 — Pull Request a develop

1. Ve a GitHub → tu repositorio
2. Verás un banner: **"feat/mi-cambio had recent pushes"** → pulsa **Compare & pull request**
3. Configura:
   - Base: `develop`
   - Compare: `feat/mi-cambio`
   - Título: `feat(backend): añadir endpoint de forecast`
4. Pulsa **Create pull request**
5. Si no requiere aprobación en `develop`, haz **Merge pull request** tú mismo
6. Borra la rama feature cuando te lo sugiera

---

## Paso 3 — Pull Request a main

1. En GitHub: **New pull request**
2. Configura:
   - Base: `main`
   - Compare: `develop`
   - Título: `release: backend v1.1.0`
3. Pulsa **Create pull request**
4. **Espera la aprobación obligatoria** de un compañero (main está protegida)
5. Una vez aprobada, haz **Merge pull request**

---

## Paso 4 — Crear tag (dispara el CI)

Este paso es el que lanza GitHub Actions automáticamente.

1. En GitHub: ve a **Releases** (menú lateral derecho) → **Draft a new release**
2. En **Choose a tag**: escribe el tag nuevo, por ejemplo `backend_v1.1.0` y selecciona **Create new tag on publish**
3. En **Target**: selecciona `main`
4. En **Release title**: `Backend v1.1.0`
5. En **Description** (opcional): describe los cambios
6. Pulsa **Publish release**

> El tag `backend_v1.1.0` coincide con el patrón `backend_*` de `ci-backend.yml`, así que GitHub Actions se dispara automáticamente.

---

## Paso 5 — Verificar que el CI ha funcionado

1. En GitHub: ve a **Actions**
2. Verás el workflow **CI Backend** ejecutándose
3. Espera a que termine con ✅ verde (tarda 5-10 min por Spark + Maven)
4. Verifica la imagen en **Packages** (menú lateral del repo): deberías ver `backend:v1.1.0` y `backend:latest`

Si falla con ❌:
- Pulsa en el workflow para ver los logs
- Los errores más comunes son problemas de build del Dockerfile
- Corrige, commitea, mergea a main y crea un tag nuevo (ej: `backend_v1.1.1`)

---

## Paso 6 — Desplegar en EC2-5

### Primera vez (configuración inicial)

Solo hay que hacer esto una vez por EC2:

```bash
# 1) Instalar Docker
sudo apt-get update -y && sudo apt-get install -y docker.io
sudo systemctl start docker && sudo systemctl enable docker

# 2) Login a GHCR (en caso de ser un repositorio privado)
#    Necesitas un PAT (Personal Access Token) con permiso read:packages
#    Créalo en: GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
echo "ghp_TU_TOKEN" | sudo docker login ghcr.io -u TU_USUARIO --password-stdin

# 3) Subir deploy-backend-ghcr.sh y .env.example a la EC2
scp -i tu-clave.pem deploy-backend-ghcr.sh .env.example ubuntu@<IP_PUBLICA>:~/backend/

# 4) Crear .env a partir del ejemplo
cd ~/backend
cp .env.example .env
nano .env
# Rellena con tus valores reales
```

### Desplegar (cada vez)

La versión a desplegar se controla desde el `.env`:

```dotenv
# En ~/backend/.env
VERSION_GHCR_BACKEND=backend_v1.1.0
```



El siguiente comando detiene/para y elimina el contenedor que esté corriendo actualmente. El 2>/dev/null evita que muestre error si no existe (primera vez). Y redesplega.
```bash
sudo docker rm -f deportedata-backend 2>/dev/null
bash ~/backend/deploy-backend-ghcr.sh
```

Salida esperada:

```
============================================
 Desplegando DEPORTEData Backend desde GHCR
 Versión .env: backend_v1.1.0
 Imagen:       ghcr.io/tu-usuario/tu-repo/backend:v1.1.0
 Env:          /home/ubuntu/backend/.env
============================================
```

### Cambiar de versión de forma especifica

Solo edita una línea del `.env` y redesplega:

```bash
nano ~/backend/.env
# Cambiar: VERSION_GHCR_BACKEND=backend_v1.2.0

sudo docker rm -f deportedata-backend
bash ~/backend/deploy-backend-ghcr.sh
```


---

## Paso 7 — Verificar el despliegue

```bash
# Health check
curl http://localhost:8000/health
curl http://localhost:8001/internal/health

# Test de conexión Spark (si el clúster está activo)
curl -X POST http://localhost:8001/internal/jobs/test

# Swagger (desde el navegador)
# API Pública:  http://<IP_PUBLICA_EC2-5>:8000/docs
# API Privada:  http://<IP_PUBLICA_EC2-5>:8001/docs (en caso de ser publica 0.0.0.0/0)

# Logs
sudo docker logs -f deportedata-backend
```

---

## Errores comunes

| Problema | Causa | Solución |
|----------|-------|----------|
| CI falla en GitHub Actions | Error de build en Dockerfile | Revisar logs en Actions, corregir y crear tag nuevo |
| `docker pull` da 403 | PAT sin permiso `read:packages` | Crear nuevo PAT con el permiso correcto |
| `docker pull` da "not found" | Tag no coincide o imagen no publicada | Verificar en Packages que la imagen existe |
| `VERSION_GHCR_BACKEND no definida` | Falta la variable en `.env` | Añadir `VERSION_GHCR_BACKEND=backend_vX.X.X` al `.env` |
| API arranca pero falla en /health | `.env` incompleto o con comentarios inline | Revisar `.env`, sin comentarios en la misma línea del valor |
| spark-submit da Connection refused | `SPARK_MASTER_IP` mal configurada en `.env` | Verificar la IP privada del master |
| Credenciales AWS expiradas | Reiniciaste el Learner Lab | Actualizar las 3 líneas AWS en `.env` y recrear contenedor |

---

## Comandos rápidos de referencia

```bash
# Ver qué imagen está corriendo
sudo docker inspect deportedata-backend | grep Image

# Ver la versión desplegada
sudo docker images | grep backend

# Ver qué versión tiene el .env
grep VERSION_GHCR_BACKEND ~/backend/.env

# Rollback a versión anterior (editar .env + redesplegar)
nano ~/backend/.env   # cambiar VERSION_GHCR_BACKEND=backend_v1.0.0
sudo docker rm -f deportedata-backend
bash ~/backend/deploy-backend-ghcr.sh

# Limpiar imágenes antiguas
sudo docker image prune -a
```