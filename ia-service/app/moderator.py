"""
Moderador de toxicidad.

Usa Detoxify('multilingual') -> unitary/multilingual-toxic-xlm-roberta para
detectar si el mensaje contiene lenguaje inapropiado. Da scores en 7
categorías. Si alguna supera el umbral, extraemos las palabras "sospechosas"
cruzando el mensaje contra una lista negra simple ES/EN y se las asignamos
a todas las categorías activas.

Razón de la lista negra: el clasificador da scores GLOBALES del mensaje,
no por palabra. Para poblar `key_words_toxic_classification` necesitamos
identificar qué palabras concretas son las ofensivas, y eso se hace mejor
con matching léxico contra una lista mantenida.

La lista es corta por diseño — amplíala en `TOXIC_LEXICON` según veas.
"""
from __future__ import annotations

import logging
import re
import unicodedata
from dataclasses import dataclass
from typing import Dict, List, Set, Tuple

from detoxify import Detoxify

logger = logging.getLogger(__name__)

# Mapeo: categorías de Detoxify -> categorías del schema de salida
CATEGORY_MAP: Dict[str, str] = {
    "toxicity": "ofensive",
    "severe_toxicity": "ofensive",
    "obscene": "vulgar",
    "threat": "threat",
    "insult": "insult",
    "identity_attack": "xenophobia",
    "sexual_explicit": "sex",
}

# Lista negra léxica. Cada entrada: palabra -> set de categorías.
# Ampliable. No es exhaustiva — el clasificador captura el resto por semántica.
TOXIC_LEXICON: Dict[str, Set[str]] = {
    # Insultos genéricos / vulgar (ES)
    "idiota": {"insult", "ofensive"},
    "imbecil": {"insult", "ofensive"},
    "estupido": {"insult", "ofensive"},
    "estupida": {"insult", "ofensive"},
    "tonto": {"insult", "ofensive"},
    "tonta": {"insult", "ofensive"},
    "gilipollas": {"insult", "vulgar", "ofensive"},
    "mierda": {"vulgar", "ofensive"},
    "joder": {"vulgar", "ofensive"},
    "cabron": {"insult", "vulgar", "ofensive"},
    "cabrona": {"insult", "vulgar", "ofensive"},
    "puta": {"vulgar", "insult", "ofensive"},
    "puto": {"vulgar", "insult", "ofensive"},
    "coño": {"vulgar", "ofensive"},
    "cono": {"vulgar", "ofensive"},
    "hijoputa": {"insult", "vulgar", "ofensive"},
    "hijodeputa": {"insult", "vulgar", "ofensive"},
    "maricon": {"insult", "xenophobia", "ofensive"},
    # Insultos genéricos (EN)
    "idiot": {"insult", "ofensive"},
    "stupid": {"insult", "ofensive"},
    "moron": {"insult", "ofensive"},
    "asshole": {"insult", "vulgar", "ofensive"},
    "shit": {"vulgar", "ofensive"},
    "fuck": {"vulgar", "ofensive"},
    "bitch": {"insult", "vulgar", "ofensive"},
    "bastard": {"insult", "vulgar", "ofensive"},
    "damn": {"vulgar", "ofensive"},
    # Contenido sexual explicito (ES/EN mínimos)
    "porno": {"sex", "vulgar"},
    "porn": {"sex", "vulgar"},
    "sexo": {"sex"},
    # Amenazas
    "matar": {"threat"},
    "matarte": {"threat"},
    "kill": {"threat"},
    # Xenofobia / ataques identidad (mínimos — añadir con cabeza)
    "sudaca": {"xenophobia", "ofensive"},
    "moro": {"xenophobia", "ofensive"},
}


@dataclass
class ModerationResult:
    has_toxic: bool
    toxic_words: List[dict]  # [{"word": str, "categories": [str, ...]}, ...]


class Moderator:
    """Carga Detoxify una sola vez al arrancar (tarda ~5-10 s)."""

    def __init__(self, threshold: float = 0.5):
        logger.info("Cargando modelo Detoxify multilingual (tarda ~10 s)...")
        self._model = Detoxify("multilingual")
        self._threshold = threshold
        logger.info("Detoxify listo.")

    @staticmethod
    def _normalize(text: str) -> str:
        """Quita acentos y pasa a minúsculas para el match léxico."""
        text = unicodedata.normalize("NFD", text)
        text = "".join(c for c in text if unicodedata.category(c) != "Mn")
        return text.lower()

    @staticmethod
    def _tokenize(text: str) -> List[str]:
        # Palabras de >= 2 letras, sin signos
        return re.findall(r"[a-zñ]{2,}", text)

    def _active_categories(self, scores: Dict[str, float]) -> Set[str]:
        active = set()
        for raw_key, mapped in CATEGORY_MAP.items():
            if float(scores.get(raw_key, 0.0)) >= self._threshold:
                active.add(mapped)
        return active

    def _find_words(
        self, normalized_message: str, classifier_categories: Set[str]
    ) -> List[dict]:
        """
        Devuelve la lista de palabras tóxicas encontradas.

        Estrategia: cruza tokens del mensaje con TOXIC_LEXICON. A cada palabra
        encontrada se le unen SUS categorías del léxico + las categorías
        activas del clasificador (el clasificador "amplifica" la clasificación).
        """
        tokens = self._tokenize(normalized_message)
        hits: List[dict] = []
        seen = set()
        for tok in tokens:
            if tok in seen:
                continue
            if tok in TOXIC_LEXICON:
                cats = set(TOXIC_LEXICON[tok]) | classifier_categories
                hits.append({"word": tok, "categories": sorted(cats)})
                seen.add(tok)
        return hits

    def moderate(self, message: str) -> ModerationResult:
        normalized = self._normalize(message)

        # 1) Clasificador semántico
        try:
            scores = self._model.predict(message)
        except Exception as exc:
            logger.exception("Detoxify predict falló: %s", exc)
            scores = {}

        classifier_cats = self._active_categories(scores)

        # 2) Cruce léxico
        word_hits = self._find_words(normalized, classifier_cats)

        # 3) Decisión: tóxico si el clasificador dispara O hay hits léxicos
        has_toxic = bool(classifier_cats) or bool(word_hits)

        # Si hubo clasificación pero ningún token cruzado, devolvemos la
        # marca global sin palabras (schema admite lista vacía).
        if has_toxic and not word_hits and classifier_cats:
            word_hits = []  # no inventamos palabras

        logger.info(
            "Moderación: scores=%s cats_activas=%s hits=%s",
            {k: round(float(v), 3) for k, v in scores.items()},
            sorted(classifier_cats),
            [h["word"] for h in word_hits],
        )
        return ModerationResult(has_toxic=has_toxic, toxic_words=word_hits)
