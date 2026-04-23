# Memoria del trabajo realizado — DEPORTEData

**Proyecto:** DEPORTEData (Reto C: previsión del empleo vinculado al deporte en España)  
**Corte de memoria:** 22 de abril de 2026  
**Base documental:** estado actual del repositorio y guías operativas incluidas.  
**Dirección HTTP:** [http://deportedata-demo.duckdns.org](http://deportedata-demo.duckdns.org) *(si las instancias EC2 del lab están en ejecución)*

---

## 1) Visión global de lo realizado

Durante el trabajo del equipo se ha construido una base **end-to-end** para el proyecto:

- Organización ágil del trabajo (Scrum ligero + Kanban + flujo Git/PR).
- Definición del problema analítico y objetivos del reto.
- Ingesta y preparación de datos de fuentes oficiales de deporte/empleo.
- Backend FastAPI con separación de API pública y privada.
- Frontend React con área pública y panel admin protegido.
- Módulo IA independiente (RAG + moderación de toxicidad).
- Estrategia de despliegue en AWS (EC2 + RDS + S3 + Spark + CloudWatch/Grafana).
- Guías de CI/CD y operación para despliegues, versionado, rollback y observabilidad.

---

## 2) Organización del proyecto y metodología

### 2.1 Marco de trabajo y gobierno

Se definió una metodología de trabajo profesional con:

- Scrum ligero por sprints semanales.
- Soporte operativo en Kanban (Backlog → Ready → In Progress → In Review → Blocked → Done).
- Trazabilidad completa Issue → PR → Merge.
- Reglas de rama y merge orientadas a calidad (`main` protegida y trabajo por `feature/*`).

### 2.2 Planificación inicial (Sprint 1)

Se documentó un Sprint 1 de inicialización con entregables de:

- definición analítica del reto;
- fuentes de datos y limpieza inicial;
- base de backend/frontend;
- primeros pasos de infraestructura.

Además, se dejó explicitado qué estaba completado y qué quedaba en progreso para sprints posteriores.

---

## 3) Trabajo de datos y analítica

### 3.1 Fuentes y materiales cargados

Se incorporaron y organizaron:

- fuentes en CSV para empleo deportivo (trimestral y anual);
- documentación contextual del problema;
- PDFs y ficheros de apoyo para el módulo IA;
- datasets transformados a JSON para recuperación semántica.

### 3.2 Preparación y limpieza

Se añadieron scripts y recursos para:

- limpieza de CSVs;
- generación de datos limpios;
- transformación de textos a formatos útiles para entrenamiento/consulta;
- base para ETL y consumo analítico.

### 3.3 Jobs de Spark

Se implementaron jobs para:

- **curación** de datasets (raw → curated/Parquet);
- **analítica** y forecast;
- **job de prueba** de conectividad (cálculo de Pi) para validar clúster.

---

## 4) Trabajo de backend

### 4.1 Arquitectura y servicios

Se implementó backend con **dos APIs FastAPI**:

- **Pública** (puerto 8000): autenticación, chat, dashboard y eventos de uso.
- **Privada** (puerto 8001): administración, jobs Spark, operaciones S3/RDS.

Esto permite separar consumo de usuario final y operaciones internas de plataforma.

### 4.2 Funcionalidades principales implementadas

- Health checks de API pública y privada.
- Login con JWT y verificación contra tabla de usuarios en MySQL.
- Registro de último login.
- Endpoint de chat que actúa como proxy limpio hacia `ia-service`.
- Registro de eventos de uso (`/usage/events`).
- Resumen de uso para admin (`/admin/usage/summary`) con autenticación.

### 4.3 Observabilidad funcional del uso

Se construyó una capa de analítica de uso que:

- crea automáticamente tabla de eventos si no existe;
- guarda tipo de evento, página, metadatos JSON, usuario/IP/user-agent;
- calcula métricas 24h/7d, actores únicos, desglose por tipo;
- explota eventos de chat para extraer y resumir toxicidad detectada.

### 4.4 Administración técnica y datos

En la API privada se añadieron endpoints para:

- lanzar jobs de Spark (curation/analytics/test);
- subir CSV/archivos a S3;
- listar claves en S3;
- listar tablas y consultar contenido en BD;
- crear tabla de usuarios e insertar usuarios con contraseña hasheada.

---

## 5) Trabajo de IA

### 5.1 Servicio IA desacoplado

Se desarrolló un microservicio FastAPI (`ia-service`) con endpoints:

- `GET /health`
- `POST /ia/chat`

Devuelve exactamente el contrato esperado con:

- `message`
- `has_toxic`
- `key_words_toxic_classification`

### 5.2 Pipeline conversacional

El flujo implementado es:

1. Moderación de entrada (Detoxify + léxico ES/EN).
2. Si hay toxicidad: respuesta segura y trazable.
3. Si no hay toxicidad: recuperación RAG en ChromaDB.
4. Generación con Ollama (Qwen) en formato JSON estructurado.

### 5.3 Base RAG

Se incorporó ingesta a ChromaDB desde `data-ia/data_json/*.json` con:

- colección recreable para cargas limpias;
- embeddings multilingües consistentes entre ingesta y consulta;
- batcheo para rendimiento.

### 5.4 Preparación de entrenamiento

También se dejó estructura de trabajo para entrenamiento/ajuste (datasets `train/val`, scripts y documentación de entrenamiento).

---

## 6) Trabajo de frontend

### 6.1 Arquitectura de la aplicación

Se construyó frontend React + Vite con:

- routing público/privado;
- `ProtectedRoute` para panel admin;
- layouts diferenciados (público y administración);
- internacionalización (i18n) y selector de idioma.

### 6.2 Área pública

Se implementó una home pública con:

- hero de producto y propuesta de valor;
- KPIs cargados por API;
- embebido de paneles de dashboard (Grafana);
- acceso al chatbot;
- tracking de uso (`public_page_view`).

### 6.3 Área admin

Se desarrolló panel admin con:

- login;
- home con métricas de uso (24h/7d, eventos, actividad chat);
- páginas de telemetría, seguridad, uso e insultos;
- consumo de resumen de uso desde backend;
- tracking de navegación admin.

### 6.4 Integración operacional

El frontend está preparado para:

- inyectar configuración en despliegue (`env-config.js`);
- apuntar a dashboards específicos por entorno;
- desplegar en contenedor y actualizar por tag de imagen.

---

## 7) Trabajo en AWS e infraestructura

## 7.1 Componentes AWS usados/documentados

La documentación y scripts reflejan un despliegue con:

- **EC2** para ejecución de servicios (frontend/back/ia y/o nodos Spark).
- **RDS MySQL** para usuarios y eventos de uso.
- **S3** como data lake (raw/processed/analytics).
- **CloudWatch** para métricas/logs técnicos.
- **Grafana** conectado a CloudWatch para visualización operativa.

### 7.2 Despliegue de backend/IA en EC2

Se dejó guía operativa para:

- preparar `.env` con credenciales y endpoints;
- desplegar por `docker compose` desde imágenes GHCR;
- arrancar `ollama`, `chromadb`, `ia-service` y `backend`;
- gestionar salud de servicios y reinicio/recreación.

### 7.3 Spark en infraestructura cloud

El backend incluye configuración para ejecutar `spark-submit` remoto con:

- master en red privada;
- puertos fijos de driver y block manager;
- credenciales AWS temporales de Learner Lab (S3A);
- validaciones y mensajes de error de operación.

### 7.4 Seguridad y operación en AWS

Se documentaron prácticas para:

- no exponer credenciales en frontend;
- mantener secretos en backend/.env;
- controlar puertos y SG para servicios necesarios;
- renovar credenciales temporales cuando el lab se reinicia.

### 7.5 Observabilidad cloud

Se separó explícitamente:

- **infraestructura/técnico** → CloudWatch + Grafana.
- **uso de producto** → RDS vía backend.

Con ello se evita mezcla de fuentes y se obtiene trazabilidad funcional + técnica.

---

## 8) CI/CD, versionado y operación

Se documentó flujo CI/CD para backend (replicable en módulos):

- feature → develop → main;
- creación de tag de release para disparar Actions;
- publicación de imágenes en GHCR;
- despliegue controlado en EC2 por variable de versión en `.env`;
- rollback cambiando tag y redeploy.

También quedaron guías para operación diaria de frontend y backend (pull, up -d, logs, health checks).

---

## 9) Estado funcional consolidado (resultado del trabajo)

A fecha de esta memoria, el repositorio muestra una solución integrada con:

- estructura de proyecto por dominios (frontend/backend/ia/deploy/docs);
- aplicación web con área pública y área admin;
- backend productivo con autenticación, chat y telemetría de uso;
- microservicio IA con moderación y RAG;
- base de jobs de datos/analítica con Spark;
- documentación de despliegue y operación en AWS.

En otras palabras, no solo se ha “hecho código”, sino también **producto + arquitectura + operación** para poder iterar por sprints con base real.

---

## 10) Próximos pasos recomendados (continuación natural)

1. Endurecer seguridad (CORS/orígenes permitidos, políticas SG mínimas, rotación de secretos).
2. Completar métricas de calidad de modelo (MAE/RMSE/MAPE) expuestas en dashboard.
3. Automatizar aún más la release multi-módulo con workflows homogéneos.
4. Añadir tests automatizados (backend + frontend + integración IA).
5. Consolidar memoria final académica con evidencias (capturas, logs y resultados analíticos).

---

## 11) Resumen ejecutivo corto para entrega

El equipo ha levantado en este trabajo una plataforma completa para DEPORTEData: se definió el marco analítico del reto, se organizó el flujo profesional de desarrollo, se construyó frontend y backend funcionales, se integró un servicio de IA con moderación y RAG, y se preparó un despliegue real en AWS con observabilidad y operación documentada. Esto deja el proyecto listo para escalar en los siguientes sprints con foco en calidad de predicción y robustez de producto.
