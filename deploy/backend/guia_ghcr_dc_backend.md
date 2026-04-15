# Guía Backend DEPORTEData (docker-compose.yml)

Guía paso a paso para cuando alguien modifica el backend: desde el commit hasta el despliegue en EC2.


---

## 1. Crear rama y hacer cambios

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

## 2. Pull Request a develop

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

## 3. Pull Request a main

1. En GitHub: **New pull request**
2. Configura:
   - Base: `main`
   - Compare: `develop`
   - Título: `release: backend v1.1.0`
3. Pulsa **Create pull request**
4. **Espera la aprobación obligatoria** de un compañero (main está protegida)
5. Una vez aprobada, haz **Merge pull request**

---

## 4. Crear tag (dispara el CI)

Este paso es el que lanza GitHub Actions automáticamente.

1. En GitHub: ve a **Releases** (menú lateral derecho) → **Draft a new release**
2. En **Choose a tag**: escribe el tag nuevo, por ejemplo `backend_v1.1.0` y selecciona **Create new tag on publish**
3. En **Target**: selecciona `main`
4. En **Release title**: `Backend v1.1.0`
5. En **Description** (opcional): describe los cambios
6. Pulsa **Publish release**

> El tag `backend_v1.1.0` coincide con el patrón `backend_*` de `ci-backend.yml`, así que GitHub Actions se dispara automáticamente.

---

## 5. Verificar que el CI ha funcionado

1. En GitHub: ve a **Actions**
2. Verás el workflow **CI Backend** ejecutándose
3. Espera a que termine  (tarda 5-10 min por Spark + Maven)
4. Verifica la imagen en **Packages** (menú lateral del repo): deberías ver `backend:v1.1.0` y `backend:latest`

Si falla:
- Pulsa en el workflow para ver los logs
- Los errores más comunes son problemas de build del Dockerfile
- Corrige, commitea, mergea a main y crea un tag nuevo (ej: `backend_v1.1.1`)

---

## Paso 6 — Desplegar en EC2-5

### Primera vez (configuración inicial)

Solo hay que hacer esto una vez por EC2:

```bash
# 1) Instalar Docker + Docker Compose
sudo apt-get update -y && sudo apt-get install -y docker.io docker-compose-v2
sudo systemctl start docker && sudo systemctl enable docker

# 2) Login a GHCR (solo si el repositorio es privado)
#    Necesitas un PAT (Personal Access Token) con permiso read:packages
#    Créalo en: GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
echo "ghp_TU_TOKEN" | sudo docker login ghcr.io -u TU_USUARIO --password-stdin

# 3) Subir docker-compose.yml y .env.example a la EC2
scp -i tu-clave.pem docker-compose.yml .env.example ubuntu@<IP_PUBLICA>:~/backend/

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
BACKEND_IMAGE_TAG=v1.1.0
```

> **Nota:** el tag de Git es `backend_v1.1.0`, pero la imagen en GHCR se publica como `backend:v1.1.0`. Por eso en el `.env` se pone solo `v1.1.0` (sin el prefijo `backend_`).

Desplegar:

```bash
cd ~/backend
sudo docker compose pull
sudo docker compose up -d
```

Salida esperada de `docker compose ps`:

```
NAME                   IMAGE                                              STATUS
deportedata-backend    ghcr.io/criscros/deportedata/backend:v1.1.0       Up 10 seconds
```

### Cambiar de versión

Edita una línea del `.env` y redesplega:

```bash
nano ~/backend/.env
# Cambiar: BACKEND_IMAGE_TAG=v1.2.0

cd ~/backend
sudo docker compose pull
sudo docker compose up -d
```

### Rollback a una versión anterior

```bash
nano ~/backend/.env
# Cambiar: BACKEND_IMAGE_TAG=v1.0.0

cd ~/backend
sudo docker compose pull
sudo docker compose up -d
```


---

## Paso 7 — Verificar el despliegue

```bash
# Estado del contenedor
cd ~/backend && sudo docker compose ps

# Health check
curl http://localhost:8000/health
curl http://localhost:8001/internal/health

# Test de conexión Spark (si el clúster está activo)
curl -X POST http://localhost:8001/internal/jobs/test

# Swagger (desde el navegador)
# API Pública:  http://<IP_PUBLICA_EC2-5>:8000/docs
# API Privada:  http://<IP_PUBLICA_EC2-5>:8001/docs (en caso de ser publica 0.0.0.0/0)

# Logs
sudo docker compose logs -f backend
```

---

## Resumen visual

```
 TU PC                    GITHUB                    EC2-5
 ─────                    ──────                    ─────

 git commit          ┌─── feat/mi-cambio
 git push ──────────▶│
                     │    PR → develop
                     │    PR → main (aprobación)
                     │
                     │    Crear tag: backend_v1.1.0
                     │         │
                     │         ▼
                     │    GitHub Actions
                     │    ┌─────────────────┐
                     │    │ docker build     │
                     │    │ docker push GHCR │
                     │    └────────┬────────┘
                     │             │
                     │             ▼
                     │    GHCR: backend:v1.1.0
                     └─────────────┬───────────
                                   │
                          .env: BACKEND_IMAGE_TAG=v1.1.0
                          docker-compose.yml
                                   │
                                   │ docker compose pull
                                   │ docker compose up -d
                                   ▼
                          ┌─────────────────────────┐
                          │  imagen (código + Spark) │
                          │  + .env (credenciales)   │
                          │  = API funcionando       │
                          └─────────────────────────┘
```

---

## Errores comunes

| Problema | Causa | Solución |
|----------|-------|----------|
| CI falla en GitHub Actions | Error de build en Dockerfile | Revisar logs en Actions, corregir y crear tag nuevo |
| `docker pull` da 403 | PAT sin permiso `read:packages` | Crear nuevo PAT con el permiso correcto |
| `docker pull` da "not found" | Tag no coincide o imagen no publicada | Verificar en Packages que la imagen existe |
| `BACKEND_IMAGE_TAG` no definida | Falta la variable en `.env` | Añadir `BACKEND_IMAGE_TAG=vX.X.X` al `.env` |
| API arranca pero falla en /health | `.env` incompleto o con comentarios inline | Revisar `.env`, sin comentarios en la misma línea del valor |
| spark-submit da Connection refused | `SPARK_MASTER_IP` mal configurada en `.env` | Verificar la IP privada del master |
| Credenciales AWS expiradas | Reiniciaste el Learner Lab | Actualizar las 3 líneas AWS en `.env` y recrear contenedor |

---

## Comandos rápidos de referencia

```bash
# Ver estado de los servicios
cd ~/backend && sudo docker compose ps

# Ver qué imagen está corriendo
sudo docker inspect deportedata-backend | grep Image

# Ver qué versión tiene el .env
grep BACKEND_IMAGE_TAG ~/backend/.env

# Logs en tiempo real
cd ~/backend && sudo docker compose logs -f backend

# Reiniciar el backend
cd ~/backend && sudo docker compose restart backend

# Parar todo
cd ~/backend && sudo docker compose down

# Rollback a versión anterior (editar .env + redesplegar)
nano ~/backend/.env   # cambiar BACKEND_IMAGE_TAG=v1.0.0
cd ~/backend
sudo docker compose pull
sudo docker compose up -d

# Limpiar imágenes antiguas
sudo docker image prune -a
```

---

## Qué hacer al reiniciar el Learner Lab

Las credenciales AWS caducan cada vez que reinicias el Lab:

```bash
# 1) Actualizar las 3 líneas de AWS en el .env
nano ~/backend/.env

# 2) Recrear el contenedor
cd ~/backend
sudo docker compose down
sudo docker compose up -d
```

Si además la IP pública de EC2-5 cambia, tendrás que reconectar por SSH con la nueva IP. La IP privada no cambia.