"""
Job 2: Analytics: Parquet curated/  -> analytics/ (tipo parquet).

Lee de curated/ y produce 4 datasets, optimizados para bulk-load a RDS MySQL desde un paso posterior.

Resultado (tipo parquet) de salidas (sin particionar — son datasets finales pequeños):
    analytics/dim_indicador/      dim_indicador (PK id_indicador)
    analytics/fact_trimestral/    serie trimestral (facts + FK id_indicador)
    analytics/fact_anual/         medias anuales
    analytics/fact_anual_mm/      medias móviles anuales (rolling 4T)
"""

import os
import sys
from pyspark.sql import SparkSession
from pyspark.sql import functions as F


# Config de rutas S3
BUCKET    = os.environ.get("S3_BUCKET_DATALAKE", "deportedata-datalake")
PROJECT   = os.environ.get("NOM_USER_ID",        "deportedata_proyect")
BASE      = f"s3a://{BUCKET}/deportedata/{PROJECT}"
CURATED   = f"{BASE}/curated"
ANALYTICS = f"{BASE}/analytics"


# Agrupaciones de datasets por frecuencia
TRIMESTRAL_DATASETS = [
    "trimestral_jornada_laboral",
    "trimestral_perfil_demografico",
]
ANUAL_DATASETS = [
    "medias_anuales_demografia",
    "medias_anuales_jornada_sexo",
    "medias_anuales_tipo_empleo",
]
ANUAL_MM_DATASETS = [
    "anual_mm_jornada",
    "anual_mm_perfil",
]


def build_dim_indicador(spark):
    """Diccionario único de indicadores con id estable por hash."""
    print("[job2] --- dim_indicador ---")
    df = spark.read.parquet(CURATED)

    dim = (
        df.select("indicador")
          .dropna()
          .distinct()
          .withColumn("id_indicador",
                      F.abs(F.hash("indicador")).cast("int"))
          .withColumn("tipo_indicador",
                      F.when(F.col("indicador").contains("En miles"), "absoluto_miles")
                       .when(F.col("indicador").contains("%"),        "porcentaje")
                       .when(F.lower(F.col("indicador")).contains("tasa"), "tasa")
                       .otherwise("otro"))
          .select("id_indicador", "indicador", "tipo_indicador")
          .orderBy("id_indicador")
    )

    out = f"{ANALYTICS}/dim_indicador"
    dim.coalesce(1).write.mode("overwrite").parquet(out)
    n = dim.count()
    print(f"[job2]   OK  dim_indicador: {n} indicadores -> {out}")
    return dim


def build_fact_trimestral(spark, dim):
    print("[job2] --- fact_trimestral ---")
    df = (
        spark.read.parquet(CURATED)
        .filter(F.col("dataset").isin(*TRIMESTRAL_DATASETS))
        .join(dim.select("id_indicador", "indicador"), on="indicador", how="left")
        .select(
            "id_indicador",
            "dataset",
            "anio",
            "trimestre",
            F.col("periodo_raw").alias("periodo"),
            "situacion_jornada",
            "sexo_edad_estudios",
            "sexo",
            "valor",
        )
    )
    out = f"{ANALYTICS}/fact_trimestral"
    df.coalesce(1).write.mode("overwrite").parquet(out)
    print(f"[job2]   OK  fact_trimestral: {df.count()} filas -> {out}")


def build_fact_anual(spark, dim):
    print("[job2] --- fact_anual ---")
    df = (
        spark.read.parquet(CURATED)
        .filter(F.col("dataset").isin(*ANUAL_DATASETS))
        .join(dim.select("id_indicador", "indicador"), on="indicador", how="left")
        .select(
            "id_indicador",
            "dataset",
            "anio",
            F.col("periodo_raw").alias("periodo"),
            "situacion_jornada",
            "sexo_edad_estudios",
            "sexo",
            "valor",
        )
    )
    out = f"{ANALYTICS}/fact_anual"
    df.coalesce(1).write.mode("overwrite").parquet(out)
    print(f"[job2]   OK  fact_anual: {df.count()} filas -> {out}")


def build_fact_anual_mm(spark, dim):
    print("[job2] --- fact_anual_mm ---")
    df = (
        spark.read.parquet(CURATED)
        .filter(F.col("dataset").isin(*ANUAL_MM_DATASETS))
        .join(dim.select("id_indicador", "indicador"), on="indicador", how="left")
        .select(
            "id_indicador",
            "dataset",
            "anio",
            F.col("periodo_raw").alias("periodo"),
            "situacion_jornada",
            "sexo_edad_estudios",
            "sexo",
            "valor",
        )
    )
    out = f"{ANALYTICS}/fact_anual_mm"
    df.coalesce(1).write.mode("overwrite").parquet(out)
    print(f"[job2]   OK  fact_anual_mm: {df.count()} filas -> {out}")


def main():
    spark = (
        SparkSession.builder
        .appName("DEPORTEData_Job2_Analytics")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")
    print(f"[job2] Spark {spark.version} — master: {spark.sparkContext.master}")
    print(f"[job2] CURATED   = {CURATED}")
    print(f"[job2] ANALYTICS = {ANALYTICS}")

    try:
        dim = build_dim_indicador(spark)
        dim.cache()  # se usa en 3 facts

        build_fact_trimestral(spark, dim)
        build_fact_anual(spark, dim)
        build_fact_anual_mm(spark, dim)

        print("\n[job2] OK — Datasets analíticos generados.")
    except Exception as e:
        print(f"[job2] ERROR: {e}", file=sys.stderr)
        spark.stop()
        sys.exit(1)

    spark.stop()


if __name__ == "__main__":
    main()
