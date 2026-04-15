# 🚀 Hoja de Ruta: Fine-Tuning de Qwen 2.5 para Datos Deportivos
Este documento resume la transición de nuestro sistema actual de RAG (Consulta a documentos) a Fine-Tuning (Entrenamiento del cerebro del modelo) aprovechando el servidor de 60 GB de VRAM.

## 💡 Concepto Clave: RAG vs. Fine-Tuning
RAG (Lo que tenemos): Examen a "libro abierto". El modelo lee los trozos de JSON en tiempo real.

Fine-Tuning (Mañana): El modelo "estudia" los datos. Ajustamos sus neuronas para que el conocimiento sobre empleo y turismo deportivo sea instintivo.

## 🏗️ Fases del Proyecto
1. Preparación del Dataset (Hoy)

No podemos entrenar con archivos sueltos. Necesitamos un archivo .jsonl en formato de instrucciones (Pares Pregunta-Respuesta).

Objetivo: Convertir nuestros 62 fragmentos actuales en ejemplos de entrenamiento.

2. Configuración del Servidor (Mañana - 60GB VRAM)

Usaremos el servidor físico para el entrenamiento pesado. El modelo elegido es Qwen 2.5 7B por su equilibrio entre razonamiento y velocidad.

Herramienta: Unsloth (Optimiza el uso de VRAM y acelera el proceso x2).

3. El Entrenamiento (Fine-Tuning)

Aplicaremos LoRA / QLoRA. No entrenamos el modelo entero (sería lentísimo), sino que le añadimos "capas inteligentes" especializadas en:

Predicción de empleo: Detectar tendencias numéricas.

Formateo Markdown: Capacidad de generar tablas limpias a partir de datos densos.

4. Publicación y Uso

Hugging Face: Subiremos nuestra versión entrenada (ej: qwen-deporte-espana).

Ollama: Convertiremos el resultado a .GGUF para que nuestro Mac lo ejecute de forma nativa.

## 🛠️ To-Do List (Lista de Tareas)
Inmediato (Hoy)

[ ] Ejecutar preparar_entrenamiento.py para generar el archivo dataset_entrenamiento.jsonl.

[ ] Verificar que los pares pregunta-respuesta incluyan ejemplos de predicción y tablas.

[ ] Guardar en un USB o nube el script entrenar_qwen.py.

En el Servidor (Mañana)

[ ] Configurar Entorno: Crear el ambiente de Conda e instalar CUDA, torch y unsloth.

[ ] Lanzar Entrenamiento: Ejecutar el script y monitorear el uso de VRAM (con 60GB iremos sobrados).

[ ] Validación: Hacerle preguntas al modelo entrenado sin usar la base de datos externa.

Finalización

[ ] Subir los weights resultantes a nuestro repositorio de Hugging Face.

[ ] Exportar a formato GGUF para compartir con el resto del equipo.

## 📦 Requisitos Técnicos en el Servidor

```bash
# Instalación rápida de dependencias
pip install torch torchvision torchaudio
pip install "unsloth[colab-bitandbytes] @ git+https://github.com/unslothai/unsloth.git"
pip install xformers trl peft accelerate bitsandbytes
Nota para el equipo: Con 60 GB de VRAM tenemos potencia para entrenar el modelo de 7B en menos de 10 minutos. El éxito depende de que nuestro Dataset sea variado y no solo una copia del texto del PDF.
```