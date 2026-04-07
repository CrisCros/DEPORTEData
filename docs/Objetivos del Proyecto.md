# Proyecto: Previsión anual de empleo vinculado al deporte  
**Equipo:** Sebastian, Silvia, Javier y Dario
**Fecha:** 7 de abril de 2026  

## Resumen Ejecutivo  
Este documento presenta los objetivos y el plan de un proyecto dirigido a **predecir la evolución anual del empleo vinculado al deporte en España**. La relevancia de este tema queda de manifiesto en cifras recientes: la industria deportiva generó 39.117 millones de € (3,3% del PIB) y casi 414.000 empleos en 2018【17†L528-L534】, y en 2025 el empleo deportivo alcanzó 270.200 personas, un 6% más que el año anterior【14†L39-L44】. Ante este crecimiento sostenido, prever su evolución futura es clave para la planificación de políticas públicas y estrategias privadas. Dado el plazo limitado, el proyecto se centrará en objetivos simples y alcanzables: reunir datos oficiales (EPA del INE gestionada por DEPORTEData【15†L59-L63】), montar un pipeline básico de análisis y emplear métodos de forecasting (ARIMA, Prophet o regresión) para generar predicciones anuales. A continuación se detallan el contexto, objetivos generales y específicos (con criterios de aceptación), alcance y limitaciones, metodología, entregables por sprint, cronograma, riesgos y mitigaciones, requisitos técnicos, criterios de éxito y anexos sugeridos.  

## 1. Contexto y motivación  
- **Importancia económica del deporte:** El sector deportivo es un motor económico relevante. Según un informe de PwC (2018), contribuyó con un 3,3% al PIB de España y con casi 414.000 empleos (~2,1% del empleo total)【17†L528-L534】. Esto refleja que por cada millón de € facturados en este sector se generan 12,4 puestos de trabajo, cifra muy superior a la media nacional.  
- **Crecimiento del empleo deportivo:** Los datos recientes confirman una tendencia al alza en el empleo vinculado al deporte. En 2025 se registraron 270.200 empleos (6,0% más que en 2024 y 15,2% más que en 2022)【14†L39-L44】. Este empleo incluye tanto las ocupaciones en empresas del sector (gimnasios, clubs, instalaciones, eventos deportivos) como los puestos de deportistas, entrenadores e instructores【14†L39-L44】. Además, el perfil laboral en el deporte es más joven y con mayor nivel formativo que el promedio nacional. En conjunto, estos hechos subrayan el dinamismo del sector.  
- **Necesidad de previsión:** Predecir el empleo deportivo puede ayudar a gobiernos y empresas a anticipar demanda de empleo y adaptar inversiones en formación, infraestructuras y políticas de promoción del deporte. Un modelo predictivo anual permitiría estimar cuántos puestos de trabajo generará el sector en los próximos años, apoyando la toma de decisiones. Dada la complejidad inherente a la economía y limitaciones de tiempo y datos, el proyecto buscará un equilibrio entre precisión y viabilidad, tal como se detalla en las secciones siguientes.

## 2. Objetivo general  
Desarrollar un sistema funcional para **predecir la evolución anual del empleo vinculado al deporte en España**, basado en datos oficiales, mediante un modelo de series temporales, y documentar el proceso de forma clara y comprensible.  

## 3. Objetivos específicos  
- **Recolectar datos oficiales de empleo deportivo:** Obtener y documentar las series temporales anuales de empleo vinculadas al deporte. *Criterio:* Disponibilidad de fichero(s) con datos EPA (INE) desde 2011 hasta el último año (DEPORTedata【15†L59-L63】) y de cualquier otra fuente oficial relevante, en formato CSV validado.  
- **Diseñar pipeline ETL básico:** Implementar scripts para limpiar, transformar y unificar los datos. *Criterio:* Script en Python que cargue las fuentes (p. ej. CSV), trate valores nulos/erróneos, y genere un dataset consolidado listo para análisis.  
- **Análisis exploratorio de datos (EDA):** Visualizar la serie histórica y características del empleo deportivo. *Criterio:* Gráficos de tendencias anuales (por ejemplo, línea de tiempo del empleo total) y análisis de patrones relevantes (temporalidad, estacionalidad si la hubiera).  
- **Desarrollar modelos predictivos:** Entrenar al menos dos modelos de forecasting, por ejemplo ARIMA y Prophet (o regresión lineal de tendencia). *Criterio:* Modelos calibrados con datos de entrenamiento (por ejemplo hasta 2023) y listos para predecir años posteriores.  
- **Validar y comparar modelos:** Evaluar la precisión con métricas (MAE, MAPE, RMSE). *Criterio:* Cálculo de métricas de error en datos de prueba (por ejemplo años 2024-2025) y selección del modelo más adecuado (menor error relativo).  
- **Seleccionar modelo final:** Elegir el modelo óptimo según precisión y simplicidad. *Criterio:* Documentar el modelo elegido con justificación basada en métricas (p. ej. MAPE < 10%) y consideraciones de interpretación.  
- **Implementar visualizaciones finales:** Crear al menos un dashboard o serie de gráficos comparando la serie histórica con la previsión. *Criterio:* Dashboard o informe con gráficos claros (por ejemplo, barras o líneas de tendencias) que muestre la proyección de empleo deportivo para los próximos años.  
- **Documentación del proyecto:** Mantener un README y documentación de apoyo. *Criterio:* Entrega de README.md con descripción del proyecto, instrucciones de uso, y archivo de diseño (arquitectura, fuentes); además de anotaciones en el código explicando cada paso.  

## 4. Alcance y limitaciones  
- **Ámbito geográfico:** El análisis se centrará en **España** a nivel nacional, no se detallará por Comunidades Autónomas o provincias.  
- **Frecuencia de datos:** Se utilizarán datos **anuales**. No se profundizará en series trimestrales o mensuales por su menor disponibilidad y complejidad añadida.  
- **Variables consideradas:** Solo se considerará el **número de empleos vinculados al deporte** (tal como lo define la EPA procesada por DEPORTEData). No se modelarán explicaciones causales (PIB, población activa, pandemia, etc.).
- **Horizonte de predicción:** Se hará una **previsión a corto plazo** (1-2 años). No se abordará forecasting a largo plazo debido a la escasez de datos históricos (EPA deportiva desde 2011) y al plazo del proyecto.
- **Complejidad de modelos:** Se priorizarán métodos sencillos y robustos (ARIMA, Prophet). No se implementarán técnicas avanzadas (redes neuronales, aprendizaje profundo) ni se llevará a cabo un ajuste extensivo de hiperparámetros.
- **Despliegue:** El alcance principal es analítico. El despliegue en producción (por ejemplo, API pública en la nube) es opcional y simplificado: si se hace, será con contenedores ligeros (Docker) o servicios gratuitos (Heroku/AWS básico).  

## 5. Metodología propuesta  
- **Fuentes de datos:** Se usarán los datos oficiales del **INE (EPA)** elaborados específicamente para el ámbito deportivo. Esto incluye la serie histórica anual del empleo deportivo (disponible en la plataforma DEPORTEData hasta 2025).  
- **Pipeline ETL:** En Python con librerías como pandas. Se extraerán los datos crudos (CSV u hoja de cálculo), se realizará la limpieza (por ejemplo, tratar valores nulos, unificar nomenclaturas de sectores) y se transformará en un único dataset con variables clave (año, empleo_total, etc.). El resultado será un dataframe anual listo para análisis.  
- **Análisis exploratorio:** Uso de gráficos (matplotlib/seaborn). Se explorará la tendencia temporal, posibles cambios bruscos, distribución por categorías (sexo, tiempo parcial/completo, según EPA) si están disponibles. Esto ayudará a entender el comportamiento histórico antes de modelar.  
- **Modelos de forecasting:** Se aplicarán al menos dos enfoques:  
  - *ARIMA (AutoRegresivo Integrado de Media Móvil):* Modelo estadístico clásico para series temporales, útil cuando la serie es estacionaria o puede estacionarizarse. Permite capturar tendencias lineales y autocorrelaciones.  
  - *Prophet:* Biblioteca de forecasting de Facebook, efectiva con tendencias y estacionalidades, y fácil de implementar.  
  - *Regresión lineal de tendencia (baseline):* Modelo simple de referencia con el año como variable independiente.  
- **Validación:** Se dividirán los datos por tiempo, reservando los años más recientes para prueba. Por ejemplo, entrenar con 2011–2023 y validar en 2024–2025. Se computarán métricas como MAE (error absoluto medio), RMSE (error cuadrático medio) y especialmente MAPE (error porcentual medio) para evaluar precisión.  
- **Selección de modelo:** Se compararán los errores y la simplicidad de cada modelo. Se elegirá el más adecuado según menor error y facilidad de explicación (p. ej. ARIMA con parámetros claros o Prophet con tendencia detectada).  
- **Visualización de resultados:** Se crearán gráficos comparativos (histórico vs predicción). Por ejemplo, un gráfico de líneas que muestre la serie real de empleo deportivo junto con la curva proyectada para los próximos años. Se evaluará también la capacidad de cada modelo para anticipar tendencias recientes.  

## 6. Entregables mínimos por sprint  
- **Sprint 1:**  
  - Repositorio inicial en GitHub con estructura de carpetas (`data/`, `scripts/`, `docs/`).  
  - Configuración de ramas (`main`, `develop`) y tablero Kanban.  
  - Catálogo preliminar de fuentes de datos (en `docs/fuentes`).  
  - Descarga y almacenamiento de datos crudos EPA/INE (p. ej. CSV en `data/raw`).  
  - Documento de objetivos generales y plan de trabajo.
  - Página Web visual.

- **Sprint 2:**  
  - Pipeline ETL básico implementado: scripts de limpieza y transformación de datos (guardando el resultado en `data/processed`).
  - Generación del dataset procesado en data/processed.
  - Análisis exploratorio inicial: gráficos de la serie histórica (por año).  
  - Implementación de un modelo base de predicción (regresión lineal).
  - Visualización basica de resultados en la web.

- **Sprint 3:**  
  - Implementación de un modelo adicional (ARIMA o Prophet, solo uno).
  - Comparación sencilla entre modelos (métrica básica).
  - Selección del modelo final (justificación simple).
  - Generación de predicciones y gráficos finales (histórico + predicción).
  - Mejora visual mínima del dashboard (claridad > diseño).
  - Documentación final (README + informe).
  - Preparación de la presentación.

## 7. Riesgos y mitigaciones  
- **Datos insuficientes o inconsistentes:** *Mitigación:* Verificar la calidad al inicio (control de nulos, años faltantes). Documentar cualquier vaciamiento. En caso de lagunas, documentar como limitación.  
- **Precisión baja del modelo:** *Mitigación:* Comparar varios modelos (ARIMA, Prophet, regresión). Ajustar parámetros básicos. Si el error es alto (MAPE > 15%), informar y centrarse en tendencias generales más que en valores exactos.  
- **Falta de tiempo / alcance excesivo:** *Mitigación:* Priorizar objetivos esenciales (datos + modelo) y recortar extras (por ejemplo, omitir predicción por subsectores o geografía detallada). Ajustar el alcance al sprint planificado.
- **Problemas técnicos (instalación de librerías, entorno):** *Mitigación:* Crear un entorno virtual (venv/conda) o contenedor Docker básico al inicio. Documentar dependencias en un `requirements.txt`.  
- **Desacuerdos en el equipo o sobrecarga de tareas:** *Mitigación:* Definir roles claros (frontend, backend, data, devops). Reuniones breves diarias (scrum) y revisión constante del Kanban. Ajuste rápido de responsabilidades si alguien se retrasa.  
- **Errores de integración:** *Mitigación:* Usar control de versiones (Git). Revisar y probar cada script por separado antes de integrarlo al pipeline. Mantener `README` actualizado para que cualquier integrante conozca el flujo de trabajo.  

## 8. Cronograma simplificado  

| Periodo | Actividades principales |
|--------|------------------------|
| **Día 1–2 (7–8 Abr)** | Confirmar Reto C y objetivos; configurar repositorio, ramas y Kanban; identificar y descargar fuentes de datos (EPA/INE); estructura base del proyecto; web inicial simple. |
| **Día 3–7 (9–13 Abr)** | Desarrollo del pipeline ETL básico (limpieza y transformación de datos); generación del dataset procesado; inicio del análisis exploratorio (gráficos simples). |
| **Día 8–12 (14–18 Abr)** | Finalizar análisis exploratorio; implementación del modelo base (regresión lineal); primeras predicciones; integración básica en la web/dashboard. |
| **Día 13–16 (19–22 Abr)** | Implementación de un modelo adicional (ARIMA o Prophet); comparación simple de modelos; selección del modelo final; generación de gráficos finales (histórico + predicción). |
| **Día 17–18 (23–24 Abr)** | Documentación final (README, informe); preparación de la presentación; revisión general del proyecto; entrega final. |

---

## Nota

Este cronograma está optimizado para un desarrollo corto, priorizando:

- Funcionalidad completa del pipeline  
- Modelo predictivo básico pero válido  
- Visualización clara de resultados  
- Documentación correcta  

*(Las fechas son aproximadas; se recomienda una revisión al inicio de cada sprint para ajustes.)*  

## 9. Requisitos técnicos mínimos  
- **Lenguaje y librerías:** Python 3.x con paquetes `pandas`, `numpy`, `statsmodels` (ARIMA), `fbprophet` o `prophet`, `scikit-learn`, `matplotlib`/`seaborn` (visualización).  
- **Entorno de desarrollo:** Jupyter Notebook o IDE (VS Code, PyCharm), con un entorno virtual (venv o conda) para gestionar dependencias.  
- **Infraestructura local:** Cualquier PC con capacidad moderada (no se requieren GPU); se procesará una serie anual pequeña, por lo que con 8 GB de RAM es suficiente.  
- **Control de versiones:** Git y GitHub para gestionar el código y colaboración. GitHub Actions para CI básica (linting o tests sencillos).  
- **Despliegue (opcional):** Contenedores Docker para portar el modelo/pipeline. Se puede usar una instancia básica en la nube (AWS EC2 t2.micro, Heroku free tier, o similar) para alojar una API que sirva las predicciones o un servidor web estático para el dashboard.  

## 10. Criterios de éxito y evaluación  
- **Precisión del modelo:** Se considerará satisfactorio lograr un error porcentual medio (MAPE) pequeño; como referencia, un MAPE inferior al 10–15% para la serie anual se valoraría positivamente.  
- **Cumplimiento de objetivos:** Éxito si se cumplen los objetivos específicos planteados: datos recolectados, pipeline funcionando y modelo operativo con métricas calculadas.  
- **Entrega de artefactos:** El proyecto debe disponer de todos los entregables mínimos: código reproducible, README claro, documentación (docs/fuentes, definición de Done, Kanban) y visualizaciones.  
- **Plazos y metodología:** Se evaluará que se haya trabajado con metodología ágil de 4 sprints, respetando el plan inicial y actualizando el Kanban.  
- **Presentación y defensa:** La solución debe ser defendible ante un profesor: modelos explicados, limitaciones justificadas y uso de fuentes oficiales adecuadas.  

## 11. Anexos sugeridos  
- **README.md:** Descripción detallada del proyecto, instrucciones de instalación/uso, arquitectura del pipeline y resumen de resultados.  
- **docs/fuentes/**: Documento con el catálogo de fuentes de datos consultadas (EPA/INE, CSD, etc.), incluyendo enlaces y descripción (al menos formatos, periodicidad, rango temporal).  
- **Definition of Done (DoD):** Listado de criterios que definen cuándo una tarea se considera completa (pruebas aprobadas, documentación actualizada, revisión de código, etc.).  
- **Kanban (GitHub Project):** Capturas o enlace al tablero de tareas con los sprints planeados y el estado de cada item.  
- **Dashboard y visualizaciones:** Código o capturas de pantalla del dashboard final (si se desarrolla), mostrando la serie histórica y la proyección.  
- **Modelo de datos (si se crea):** Ejemplo de esquema relacional o tabla analítica final con las variables clave.  

## 12. Recomendaciones y primeros pasos inmediatos  
1. **Confirmar Reto C con el equipo:** Asegurarse de que todos comprenden que el proyecto se centrará en la previsión de empleo deportivo, y asignar roles iniciales (data, modelado, devops, etc.).  
2. **Recopilar datos oficiales:** Localizar y descargar las series de empleo deportivo (EPA/INE vía DEPORTEData, informes CSD 2020-2025). Guardar las fuentes originales y documentarlas en `docs/fuentes`.  
3. **Configurar el repositorio:** Crear el repositorio Git, definir ramas (`main`, `develop`), proteger la principal y abrir el tablero Kanban. Añadir etiquetas y plantillas (issue, PR).  
4. **Desarrollar pipeline básico:** Escribir un primer script (Python) que cargue los datos crudos descargados y genere un archivo limpio (ej. `data/processed/empleo_deportivo.csv`). Verificar la integridad de los datos procesados.  
5. **Diseñar modelo de datos y plan de análisis:** En el README inicial o documento de planificación, bosquejar el modelo analítico (columnas esperadas) y la estrategia de modelado (qué métodos se probarán). Esto servirá de guía para el primer sprint.  
