# DEPORTEData · Sprint 1 — Planificación y Ejecución (Reto C)

## Contexto operativo

- Proyecto: **DEPORTEData**  
- Reto seleccionado: **Reto C — Predicción del empleo vinculado al deporte en España**   
- Metodología: **Scrum ligero con soporte Kanban**  
- Equipo:  
  - Frontend  
  - Backend  
  - IA  
  - DevOps  

El Sprint 1 se ha planteado como un sprint de **inicialización del proyecto**, cuyo objetivo principal ha sido establecer una base técnica, organizativa y analítica suficientemente sólida para permitir el desarrollo acelerado en los siguientes sprints.

---

## Objetivo del Sprint 1

El objetivo del Sprint 1 ha sido **poner en funcionamiento el proyecto en todas sus capas principales**, sin buscar aún resultados finales, sino garantizando:

- definición clara del alcance y objetivos;
- disponibilidad de datos reales;
- base técnica inicial (frontend, backend, infraestructura);
- inicio del enfoque analítico y del modelo;
- organización del trabajo mediante herramientas colaborativas.

Este enfoque permite reducir riesgos en fases posteriores y asegurar una evolución controlada del proyecto.

---

## Alcance del Sprint 1

### Incluye

- Definición del problema y objetivos del Reto C  
- Creación y configuración del repositorio en GitHub  
- Configuración del tablero Kanban y flujo de trabajo  
- Desarrollo inicial del frontend (estructura funcional)  
- Inicio del backend (definición de endpoints básicos)  
- Recolección de datos oficiales (EPA/INE)  
- Inicio del proceso de limpieza y depuración de datos  
- Evaluación preliminar de modelos de predicción  
- Inicio de la configuración del entorno técnico (cluster/infrastructura)  

---

## Épicas del Sprint 1

### ÉPICA E1 — Definición del problema y objetivos

**Descripción:**  
Establecer el marco conceptual del proyecto, definiendo el objetivo principal, los objetivos específicos y el alcance realista del Reto C.

**Resultados alcanzados:**
- Definición del objetivo general del proyecto  
- Redacción de objetivos específicos priorizados  
- Identificación de limitaciones del proyecto  
- Elaboración del cronograma inicial  

**Estado:** Completado  

---

### ÉPICA E2 — Recolección y comprensión de datos

**Descripción:**  
Identificar, descargar y analizar las fuentes de datos necesarias para el proyecto.

**Resultados alcanzados:**
- Identificación de datasets oficiales (EPA, INE, DEPORTEData)  
- Descarga de múltiples conjuntos de datos en formato CSV  
- Organización inicial en estructura `data/raw/`  
- Análisis preliminar de variables disponibles  

**Trabajo en curso:**
- Limpieza y normalización de datos  
- Evaluación de consistencia entre datasets  

**Estado:** En progreso  

---

### ÉPICA E3 — Desarrollo inicial del backend

**Descripción:**  
Crear la base del backend para permitir la gestión y futura exposición de datos y predicciones.

**Resultados alcanzados:**
- Definición de la estructura del backend  
- Implementación inicial de endpoints básicos  
- Preparación para conexión con datos procesados  

**Trabajo en curso:**
- Integración con datasets  
- Estabilización del formato de respuesta  

**Estado:** En progreso  

---

### ÉPICA E4 — Desarrollo inicial del frontend

**Descripción:**  
Construir una interfaz básica que permita visualizar información del proyecto.

**Resultados alcanzados:**
- Creación de la estructura web inicial  
- Implementación de una primera visualización  
- Preparación para integración con datos dinámicos
  
- **Trabajo en curso:**
- Despliegue de la web


**Estado:** En progreso  

---

### ÉPICA E5 — Selección del modelo analítico

**Descripción:**  
Definir el enfoque de predicción a utilizar en el proyecto.

**Resultados alcanzados:**
- Evaluación de modelos candidatos (regresión, ARIMA, Prophet)  
- Selección preliminar de enfoque base  
- Definición de estrategia de modelado

**Trabajo en curso:**
- Implementación del modelo baseline  

**Estado:** En progreso  

---

### ÉPICA E6 — Infraestructura y entorno técnico

**Descripción:**  
Preparar el entorno necesario para ejecutar y escalar el proyecto.

**Resultados alcanzados:**
- Inicio de la configuración del entorno (cluster)  
- Definición inicial de dependencias del proyecto  
- Organización estructural del repositorio  

**Trabajo en curso:**
- Configuración completa del entorno  
- Evaluación de necesidad real de infraestructura avanzada  

**Estado:** En progreso  

---

## Lista de issues y estado

### EPIC-01 · Definición del alcance del Reto C  
**Estado:** Completado  

**Criterios cumplidos:**
- Documento de objetivos definido  
- Alcance realista establecido  
- Cronograma inicial desarrollado  

---

### EPIC-02 · Recolección de datos  
**Estado:** En progreso  

**Progreso:**
- Identificación de fuentes oficiales  
- Descarga de datasets  

**Pendiente:**
- Finalización de la limpieza de datos  
- Consolidación de dataset base  

---

### EPIC-03 · Backend inicial  
**Estado:** En progreso  

**Progreso:**
- Estructura backend definida  
- Endpoints básicos creados  

**Pendiente:**
- Conexión con datos reales  
- Validación de respuestas  

---

### EPIC-04 · Frontend inicial  
**Estado:** Completado  

**Progreso:**
- Estructura web funcional  
- Visualización básica implementada  

---

### EPIC-05 · Modelo predictivo  
**Estado:** En progreso  

**Progreso:**
- Evaluación de modelos  
- Definición del enfoque  

**Pendiente:**
- Implementación del modelo baseline  

---

### EPIC-06 · Infraestructura  
**Estado:** En progreso  

**Progreso:**
- Inicio del cluster  
- Configuración inicial  

**Pendiente:**
- Entorno completamente operativo  

---

## Evaluación del Sprint 1

### Logros principales

El Sprint 1 ha permitido:

- Establecer una base organizativa sólida mediante GitHub y Kanban  
- Definir claramente el problema, los objetivos y el alcance del proyecto  
- Disponer de datos reales procedentes de fuentes oficiales  
- Iniciar el desarrollo de todas las capas del sistema (frontend, backend, IA, infraestructura)  
- Avanzar en la comprensión del dataset y su estructura  

---

### Limitaciones detectadas

- El proceso de limpieza de datos no se ha completado  
- No existe aún un dataset procesado consolidado  
- El backend no está conectado a datos reales  
- El modelo predictivo no ha sido implementado  
- La infraestructura no está completamente operativa  

Estas limitaciones son coherentes con la naturaleza del sprint, centrado en inicialización.

---

### Riesgos identificados

- Complejidad en la unificación de datasets con diferentes estructuras  
- Limitación temporal para implementar modelos avanzados  
- Riesgo de sobrecarga en la infraestructura sin necesidad real  
- Alcance excesivo del chatbot respecto a los datos disponibles  

---

## Conclusión del Sprint 1

El Sprint 1 ha cumplido su propósito principal: **establecer una base técnica, organizativa y analítica sólida sobre la que construir el proyecto**.

A pesar del corto periodo de ejecución, se ha logrado avanzar de forma paralela en todos los componentes clave:

- datos,  
- backend,  
- frontend,  
- modelo,  
- infraestructura.  

Este enfoque permite abordar el Sprint 2 con una base estructurada, reduciendo incertidumbre y facilitando la integración progresiva de los distintos componentes.

El proyecto se encuentra en una fase inicial, pero correctamente orientado, con una planificación realista y un avance equilibrado entre áreas técnicas.
