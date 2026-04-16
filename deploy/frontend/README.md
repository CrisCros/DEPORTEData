## Despliegue Frontend

Archivos en EC2:
- `docker-compose.yml`
- `.env`

Comandos útiles:

```bash
# Ir al directorio del frontend
cd ~/frontend

# Ver la versión configurada
grep FRONTEND_IMAGE_TAG .env

# Descargar la imagen configurada
sudo docker compose pull

# Levantar o actualizar el contenedor
sudo docker compose up -d

# Forzar recreación tras cambiar variables del .env
sudo docker compose up -d --force-recreate

# Ver estado
sudo docker compose ps

# Ver logs
sudo docker compose logs --tail=100 frontend
```

Cambio de versión manual:

```bash
cd ~/frontend
nano .env
# Cambiar FRONTEND_IMAGE_TAG=vX.Y.Z
sudo docker compose pull
sudo docker compose up -d
```

Rollback:

```bash
cd ~/frontend
nano .env
# Volver a una versión anterior en FRONTEND_IMAGE_TAG
sudo docker compose pull
sudo docker compose up -d
```
