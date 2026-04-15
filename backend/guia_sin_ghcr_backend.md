# Guía despliegue de backend.zip en Lab

El ZIP funciona tal cual en cualquier EC2. El código no depende de puertos del Security Group ni de IPs concretas. Solo hay que configurar dos cosas: los puertos y el `.env`.

---

## 2. Configurar el .env

Tras descomprimir el ZIP en EC2-5:

```bash
unzip backend.zip
cd ~/backend
cp .env.example .env
nano .env
```

### Variables que DEBES cambiar

| Variable | Qué poner |
|----------|-----------|
| `SPARK_MASTER_IP` | La IP **privada** de tu EC2-1 (master) |
| `DB_HOST` | Tu endpoint RDS (cuando lo tengas; si no, déjalo como `localhost`) |
| `DB_PASSWORD` | Tu contraseña de RDS |
| `AWS_ACCESS_KEY_ID` | Tu credencial del Learner Lab → AWS Details → Show |
| `AWS_SECRET_ACCESS_KEY` | Tu credencial del Learner Lab → AWS Details → Show |
| `AWS_SESSION_TOKEN` | Tu credencial del Learner Lab → AWS Details → Show |

### Variables a tener en cuenta para cambiar

| Variable | Si cada uno tiene su propio Lab 
|----------|-------------------------------|
| `NOM_USER_ID` | Cambia a tu ID (actualmente: proyecto_deportedata)
| `S3_BUCKET_DATALAKE` | Cambia al nombre de tu bucket 
| `DB_NAME` | Cambia si tu BD se llama diferente 

---

## 3. Desplegar

```bash
bash ~/backend/deploy-backend.sh
```

---

## 4. Verificar

```bash
curl http://localhost:8000/health
curl http://localhost:8001/internal/health
```

Ambos deben devolver:

```json
{"status": "ok", "nom_user_id": "..."}
```

---

## Resumen rápido

```
1. Abrir puertos: 22, 80, 5000, 7077, 7000-7010, 8000, 8001, 8080, 3306, todo el tráfico (SG)
2. unzip deportedata-backend.zip
3. cp .env.example .env && nano .env  (rellenar valores)
4. bash deploy-backend.sh
5. curl http://localhost:8000/health
```

---

## Comandos útiles

```bash
# Ver logs en tiempo real
sudo docker logs -f deportedata-backend

# Reiniciar el contenedor
sudo docker restart deportedata-backend

# Parar y eliminar
sudo docker rm -f deportedata-backend

# Reconstruir (si cambias código)
sudo docker rm -f deportedata-backend
cd ~/deportedata-backend
sudo docker build -t deportedata-backend:latest .
bash ~/deportedata-backend/deploy-backend.sh
```

---

## Qué hacer al reiniciar el Lab

Las credenciales AWS caducan cada vez que reinicias el Lab:

```bash
# 1) Actualizar las 3 líneas de AWS en el .env
nano ~/deportedata-backend/.env

# 2) Recrear el contenedor
sudo docker rm -f deportedata-backend
bash ~/deportedata-backend/deploy-backend.sh
```

Si además la IP pública de EC2-5 (backend) cambia, tendrás que reconectar por SSH con la nueva IP. La IP privada no cambia.

---