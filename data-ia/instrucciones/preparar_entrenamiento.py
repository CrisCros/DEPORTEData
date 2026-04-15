import json
import os

def generar_dataset_instrucciones():
    # Rutas de tus JSON actuales
    archivos = ["data_json/dep_empleo.json", "data_json/dep_turismo.json", "data_json/dep_empre.json"]
    dataset = []

    for nombre_archivo in archivos:
        if not os.path.exists(nombre_archivo): continue
        
        with open(nombre_archivo, "r", encoding="utf-8") as f:
            data = json.load(f)
            for chunk in data["chunks"]:
                # Creamos una entrada de entrenamiento por cada fragmento
                # Esto enseña al modelo a extraer datos de empleo y predecirlos
                entrada = {
                    "instruction": "Analiza los datos estadísticos deportivos y responde con precisión técnica.",
                    "input": f"Basándote en el siguiente texto: {chunk['texto']}",
                    "output": f"El dato clave en este fragmento sobre {data['archivo_origen']} es que detalla valores relacionados con el sector deportivo, facilitando la comprensión de tendencias de empleo y actividad económica."
                }
                dataset.append(entrada)

    # Guardar en formato JSONL (una línea por cada ejemplo)
    with open("dataset_entrenamiento.jsonl", "w", encoding="utf-8") as f:
        for item in dataset:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    print(f"✅ Dataset listo con {len(dataset)} ejemplos de entrenamiento.")

if __name__ == "__main__":
    generar_dataset_instrucciones()