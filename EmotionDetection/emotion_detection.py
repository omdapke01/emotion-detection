"""Utilities for detecting emotions from customer feedback text."""

from __future__ import annotations

from typing import Any

import requests

EMOTION_API_URL = (
    "https://sn-watson-emotion.labs.skills.network/"
    "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
)
MODEL_ID = "emotion_aggregated-workflow_lang_en_stock"


def emotion_detector(text_to_analyze: str) -> dict[str, Any]:
    """Return Watson emotion scores and the dominant emotion for input text."""
    if not text_to_analyze or not text_to_analyze.strip():
        return _empty_emotion_result("invalid_text")

    headers = {"grpc-metadata-mm-model-id": MODEL_ID}
    payload = {"raw_document": {"text": text_to_analyze}}

    try:
        response = requests.post(
            EMOTION_API_URL,
            headers=headers,
            json=payload,
            timeout=15,
        )
    except requests.RequestException:
        return _empty_emotion_result("service_unavailable")

    if response.status_code == 400:
        return _empty_emotion_result("invalid_text")

    response.raise_for_status()
    emotions = response.json()["emotionPredictions"][0]["emotion"]
    dominant_emotion = max(emotions, key=emotions.get)

    return {
        "anger": emotions.get("anger"),
        "disgust": emotions.get("disgust"),
        "fear": emotions.get("fear"),
        "joy": emotions.get("joy"),
        "sadness": emotions.get("sadness"),
        "dominant_emotion": dominant_emotion,
        "error": None,
    }


def _empty_emotion_result(error: str) -> dict[str, Any]:
    """Return a normalized empty result for handled error states."""
    return {
        "anger": None,
        "disgust": None,
        "fear": None,
        "joy": None,
        "sadness": None,
        "dominant_emotion": None,
        "error": error,
    }
