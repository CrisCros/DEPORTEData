from __future__ import annotations

import logging
from functools import lru_cache
from pathlib import Path

import pandas as pd
from fastapi import HTTPException

from app.core.config import DATA_DIR, FALLBACK_DATA_DIR

ANNUAL_FILE_NAME = "medias_anuales_demografia.csv"
ABSOLUTE_INDICATOR = "EMPLEO VINCULADO AL DEPORTE: Valores absolutos (En miles)"
TOTAL_SEGMENT = "TOTAL"

logger = logging.getLogger(__name__)


class DataService:
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir

    def _dataset_path(self) -> Path:
        preferred = self.data_dir / ANNUAL_FILE_NAME
        if preferred.exists():
            return preferred

        fallback = FALLBACK_DATA_DIR / ANNUAL_FILE_NAME
        if fallback.exists():
            return fallback

        raise ValueError(
            f"No se encontró el dataset '{ANNUAL_FILE_NAME}' en '{self.data_dir}' ni en '{FALLBACK_DATA_DIR}'."
        )

    def load_raw_data(self) -> pd.DataFrame:
        csv_path = self._dataset_path()

        for encoding in ("utf-8", "latin-1"):
            try:
                df = pd.read_csv(csv_path, sep=",", encoding=encoding)
                break
            except UnicodeDecodeError:
                continue
        else:
            raise ValueError("No se pudo leer el CSV con una codificación soportada (utf-8/latin-1).")

        df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
        logger.info("CSV cargado desde %s con %s filas", csv_path, len(df))

        required_columns = {"indicador", "sexo_edad_estudios", "periodo", "valor"}
        missing = required_columns - set(df.columns)
        if missing:
            raise ValueError(f"Faltan columnas requeridas en CSV: {', '.join(sorted(missing))}.")

        if df[list(required_columns)].isnull().any().any():
            raise ValueError("Se detectaron nulos en columnas críticas: indicador/sexo_edad_estudios/periodo/valor.")

        return df

    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        # Filtrado estricto para evitar mezclar magnitudes incompatibles.
        filtered = df[
            (df["indicador"].astype(str).str.strip() == ABSOLUTE_INDICATOR)
            & (df["sexo_edad_estudios"].astype(str).str.upper().str.strip() == TOTAL_SEGMENT)
        ].copy()

        if filtered.empty:
            raise ValueError("No hay filas del indicador absoluto para TOTAL tras filtrar el dataset.")

        filtered["year"] = pd.to_numeric(
            filtered["periodo"].astype(str).str.extract(r"(\d{4})", expand=False),
            errors="coerce",
        )
        filtered["value"] = pd.to_numeric(
            filtered["valor"].astype(str).str.replace(",", ".", regex=False),
            errors="coerce",
        )

        if filtered[["year", "value"]].isnull().any().any():
            raise ValueError("Hay filas con año o valor no numérico tras conversión.")

        # Descartamos valores imposibles.
        filtered = filtered[filtered["value"] >= 0]

        # Resolución determinista de duplicados por año.
        annual = filtered.groupby("year", as_index=False)["value"].mean().sort_values("year")

        if annual.empty:
            raise ValueError("No hay datos válidos de empleo tras limpieza y agregación.")

        annual["year"] = annual["year"].astype(int)
        annual["value"] = annual["value"].astype(float)

        logger.info("Filas tras limpieza: %s; años únicos: %s", len(annual), annual["year"].nunique())
        return annual.reset_index(drop=True)

    def get_series(self) -> list[dict]:
        raw = self.load_raw_data()
        clean = self.clean_data(raw)
        return [
            {"year": int(row.year), "value": round(float(row.value), 1)}
            for row in clean.itertuples(index=False)
        ]

    def get_kpis(self) -> dict:
        series = self.get_series()
        latest = series[-1]
        previous = series[-2] if len(series) > 1 else latest
        previous_value = previous["value"]

        growth_pct = ((latest["value"] - previous_value) / previous_value * 100) if previous_value else 0.0

        return {
            "empleo_total": round(float(latest["value"]), 1),
            "growth_pct": round(float(growth_pct), 2),
            "latest_year": int(latest["year"]),
            "latest_values": series[-5:],
        }

    # Backward compatibility with current routes.
    def dashboard_series(self) -> list[dict]:
        try:
            return self.get_series()
        except ValueError as error:
            logger.error("Error validando serie: %s", error)
            raise HTTPException(status_code=500, detail=str(error)) from error

    def dashboard_kpis(self) -> dict:
        try:
            return self.get_kpis()
        except ValueError as error:
            logger.error("Error validando KPIs: %s", error)
            raise HTTPException(status_code=500, detail=str(error)) from error

    def answer_chat(self, message: str) -> str:
        clean_msg = message.lower()
        kpis = self.get_kpis()
        series = self.get_series()

        if "crec" in clean_msg or "sub" in clean_msg or "baj" in clean_msg:
            trend = "creció" if kpis["growth_pct"] >= 0 else "disminuyó"
            return (
                f"Entre {series[-2]['year']} y {kpis['latest_year']}, el empleo deportivo {trend} "
                f"un {abs(kpis['growth_pct'])}% y cerró en {kpis['empleo_total']} miles de personas."
            )

        if "año" in clean_msg or "serie" in clean_msg or "histor" in clean_msg:
            first_year = series[0]["year"]
            last_year = series[-1]["year"]
            return (
                f"Tengo datos anuales desde {first_year} hasta {last_year}. "
                f"El valor más reciente es {kpis['empleo_total']} miles de personas en {kpis['latest_year']}."
            )

        return (
            f"El último dato de empleo deportivo es {kpis['empleo_total']} miles en {kpis['latest_year']}, "
            f"con una variación interanual de {kpis['growth_pct']}%."
        )


@lru_cache
def get_data_service() -> DataService:
    return DataService(data_dir=DATA_DIR)
