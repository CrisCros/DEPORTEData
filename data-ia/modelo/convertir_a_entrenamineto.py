import json

# --- BLOQUES DE DATOS LIMPIOS (Tus fuentes de verdad) ---
data_empleo = """
[TABLA DE DATOS: EMPLEO 2022-2025]
| Categoría | 2022 | 2025 | Variación |
| :--- | :---: | :---: | :---: |
| TOTAL | 234,6 | 270,2 | +15,2% |
"""

data_turismo = """
[TABLA DE DATOS: TURISMO DEPORTIVO 2024]
| Origen | Viajes (Miles) | Gasto (M€) |
| :--- | :---: | :---: |
| Nacional | 3.830,0 | 1.275,5 |
| Internacional | 1.473,0 | 1.772,0 |
"""

data_edu = """
[TABLA DE DATOS: FORMACIÓN 2023-2024]
| Especialidad | Alumnado | % del total |
| :--- | :---: | :---: |
| Fútbol | 4.848 | 43,7% |
| Montaña | 1.054 | 9,5% |
"""

# --- CONSTRUCCIÓN DEL DATASET ---
dataset = []

# Añadimos ejemplos de EMPLEO
dataset.append({
    "instruction": "Genera una tabla de evolución de empleo y predice 2026.",
    "input": data_empleo,
    "output": "| Año | Empleados |\n|---|---|\n| 2022 | 234,6 |\n| 2025 | 270,2 |\n\nPredicción 2026: 286,4 mil (basado en tendencia +6%)."
})

# Añadimos ejemplos de TURISMO
dataset.append({
    "instruction": "Compara el gasto del turista nacional vs internacional en 2024.",
    "input": data_turismo,
    "output": "El turista internacional gasta más en total (1.772 M€) que el nacional (1.275,5 M€), a pesar de realizar menos viajes."
})

# Añadimos ejemplos de EDUCACIÓN
dataset.append({
    "instruction": "Crea una tabla con las especialidades formativas más demandadas.",
    "input": data_edu,
    "output": "| Especialidad | Alumnos |\n|---|---|\n| Fútbol | 4.848 |\n| Montaña | 1.054 |"
})

# --- GUARDAR EL ARCHIVO PARA EL SERVIDOR ---
with open("dataset_final_mañana.jsonl", "w", encoding="utf-8") as f:
    for linea in dataset:
        f.write(json.dumps(linea, ensure_ascii=False) + "\n")

print("🚀 ¡LISTO! Mañana sube 'dataset_final_mañana.jsonl' al servidor de 60GB.")