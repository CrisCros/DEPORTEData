# Admin, uso y observabilidad

Esta guia separa que datos van por CloudWatch/Grafana y que datos van por RDS.

## Arquitectura

```text
Frontend admin
  |-- iframe Grafana -> CloudWatch: infraestructura, logs y metricas tecnicas
  `-- /api/admin/usage/summary -> Backend -> RDS: uso de plataforma
```

El frontend nunca debe conectarse directo a RDS. Las credenciales de base de datos se quedan en el backend.

## Uso de plataforma en RDS

El backend registra eventos en la tabla configurada con:

```env
NAME_TABLE_USAGE_EVENTS=deportedata_usage_events
```

La tabla se crea automaticamente cuando llega el primer evento o cuando se consulta el resumen.

Eventos actuales:

- `public_page_view`: visita a la home publica.
- `admin_page_view`: visita a una pagina privada del admin.
- `login_success`: login correcto.
- `chat_message_sent`: pregunta enviada al chatbot con respuesta correcta.

Endpoint que usa el frontend admin:

```http
GET /admin/usage/summary
Authorization: Bearer <JWT>
```

Endpoint publico para registrar eventos simples:

```http
POST /usage/events
Content-Type: application/json

{
  "event_type": "public_page_view",
  "page": "/",
  "metadata": {
    "section": "home"
  }
}
```

## CloudWatch + Grafana

Usa CloudWatch para la parte tecnica:

- CPU de EC2.
- NetworkIn / NetworkOut.
- StatusCheckFailed.
- Logs de backend/frontend si se envian a CloudWatch Logs.
- Alarmas de infraestructura.

En Grafana:

1. Anade CloudWatch como datasource.
2. Configura la region del Learner Lab, normalmente `us-east-1`.
3. Usa credenciales del Lab o un rol IAM si tu entorno lo permite.
4. Crea dashboards para:
   - frontend EC2,
   - backend EC2,
   - logs/errores,
   - alarmas.
5. Copia la URL del dashboard o panel.
6. Ponla en el `.env` del frontend desplegado:

```env
VITE_ADMIN_HOME_DASHBOARD_URL=http://<grafana-host>:3000/d/...
VITE_ADMIN_TELEMETRY_DASHBOARD_URL=http://<grafana-host>:3000/d/...
VITE_ADMIN_SECURITY_DASHBOARD_URL=http://<grafana-host>:3000/d/...
VITE_ADMIN_USAGE_DASHBOARD_URL=http://<grafana-host>:3000/d/...
```

Despues recrea el contenedor del frontend para regenerar `env-config.js`:

```bash
cd ~/frontend
sudo docker compose up -d --force-recreate
```

## Siguiente mejora recomendada

Si necesitas mas detalle de uso, registra eventos adicionales desde el frontend:

- click en dashboard publico,
- apertura del chatbot,
- errores de carga,
- descarga de datos,
- cambio de idioma.

Si necesitas auditoria real, registra los eventos sensibles desde backend, no desde frontend.
