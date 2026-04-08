import pandas as pd
import os
import glob

RAW = "resources_csv"
OUT = "clean_data"
os.makedirs(OUT, exist_ok=True)


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def fix_valor(series):
    return (
        series.astype(str)
        .str.replace(",", ".", regex=False)
        .pipe(pd.to_numeric, errors="coerce")
    )


def buscar_y_leer(patron):
    """Busca el archivo de forma muy flexible y elige el mejor separador."""
    # Convertimos el patrón a algo que acepte cualquier cosa entre palabras
    # Ejemplo: "MEDIAS ANUALES" -> "*MEDIAS*ANUALES*"
    query = f"{RAW}/*{patron.replace(' ', '*').replace('_', '*')}*.csv"
    archivos = glob.glob(query)

    if not archivos:
        print(f"⚠️ No se encontró: {patron}")
        return None

    path = archivos[0]
    encodings = ["utf-8-sig", "latin-1"]
    separadores = [";", ","]

    mejor_df = None
    max_cols = 0

    for enc in encodings:
        for sep in separadores:
            try:
                df_temp = pd.read_csv(path, sep=sep, encoding=enc, nrows=5)
                if df_temp.shape[1] > max_cols:
                    max_cols = df_temp.shape[1]
                    mejor_df = pd.read_csv(path, sep=sep, encoding=enc)
            except:
                continue

    if mejor_df is not None:
        mejor_df.columns = mejor_df.columns.str.strip()
        print(f"✅ OK: {os.path.basename(path)[:40]}...")
        return mejor_df
    return None


def guardar_csv(df, columnas_nuevas, nombre_salida):
    if df is None: return
    if len(df.columns) == len(columnas_nuevas):
        df.columns = columnas_nuevas
        df["valor"] = fix_valor(df["valor"])
        df.to_csv(f"{OUT}/{nombre_salida}", index=False)
    else:
        print(f"❌ Error columnas en {nombre_salida}: Tiene {len(df.columns)}, esperamos {len(columnas_nuevas)}")


# ─────────────────────────────────────────────────────────────────────────────
# PROCESAMIENTO (Patrones ultra-flexibles)
# ─────────────────────────────────────────────────────────────────────────────

# 1. Trimestral Perfil
guardar_csv(buscar_y_leer("TRIMESTRALES*sexo"),
            ["indicador", "sexo_edad_estudios", "periodo", "valor"], "trimestral_perfil_demografico.csv")

# 2. Trimestral Jornada
guardar_csv(buscar_y_leer("TRIMESTRALES*situación"),
            ["indicador", "situacion_jornada", "periodo", "valor"], "trimestral_jornada_laboral.csv")

# 3. Anual MM Jornada
guardar_csv(buscar_y_leer("MÓVILES*situación"),
            ["indicador", "situacion_jornada", "periodo", "valor"], "anual_mm_jornada.csv")

# 4. Anual MM Perfil
guardar_csv(buscar_y_leer("MÓVILES*sexo"),
            ["indicador", "sexo_edad_estudios", "periodo", "valor"], "anual_mm_perfil.csv")

# 5. Medias Anuales - Jornada y Sexo (Buscamos "sexo" y "jornada" o "según")
guardar_csv(buscar_y_leer("ANUALES*jornada*sexo"),
            ["indicador", "situacion_jornada", "sexo", "periodo", "valor"], "medias_anuales_jornada_sexo.csv")

# 6. Medias Anuales - Principal y Secundario
guardar_csv(buscar_y_leer("principal*secundario"),
            ["indicador", "sexo", "periodo", "valor"], "medias_anuales_tipo_empleo.csv")

# 7. Medias Anuales - Demografía
# Buscamos el que dice "ANUALES", "sexo" pero NO "jornada"
archivos_anuales = glob.glob(f"{RAW}/*ANUALES*sexo*.csv")
filtro = [a for a in archivos_anuales if "jornada" not in a.lower() and "principal" not in a.lower()]
if filtro:
    df = buscar_y_leer(os.path.basename(filtro[0]).replace(".csv", ""))
    guardar_csv(df, ["indicador", "sexo_edad_estudios", "periodo", "valor"], "medias_anuales_demografia.csv")

print(f"\n🚀 Proceso completado. Revisa la carpeta '{OUT}'")