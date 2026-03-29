"""Tests for the Watson emotion detector package."""

from __future__ import annotations

from unittest.mock import Mock, patch

from requests.exceptions import Timeout

from EmotionDetection import emotion_detector


@patch("EmotionDetection.emotion_detection.requests.post")
def test_emotion_detector_returns_dominant_emotion(mock_post):
    """The helper should format the dominant emotion from the API response."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "emotionPredictions": [
            {
                "emotion": {
                    "anger": 0.1,
                    "disgust": 0.05,
                    "fear": 0.08,
                    "joy": 0.72,
                    "sadness": 0.05,
                }
            }
        ]
    }
    mock_post.return_value = mock_response

    result = emotion_detector("I am so happy we launched this product!")

    assert result == {
        "anger": 0.1,
        "disgust": 0.05,
        "fear": 0.08,
        "joy": 0.72,
        "sadness": 0.05,
        "dominant_emotion": "joy",
        "error": None,
    }


@patch("EmotionDetection.emotion_detection.requests.post")
def test_emotion_detector_handles_invalid_text(mock_post):
    """The helper should normalize invalid input responses."""
    mock_response = Mock()
    mock_response.status_code = 400
    mock_post.return_value = mock_response

    result = emotion_detector("   ")

    assert result == {
        "anger": None,
        "disgust": None,
        "fear": None,
        "joy": None,
        "sadness": None,
        "dominant_emotion": None,
        "error": "invalid_text",
    }


@patch("EmotionDetection.emotion_detection.requests.post")
def test_emotion_detector_handles_service_timeout(mock_post):
    """The helper should distinguish API/network failures from invalid text."""
    mock_post.side_effect = Timeout

    result = emotion_detector("This is a real sentence.")

    assert result == {
        "anger": None,
        "disgust": None,
        "fear": None,
        "joy": None,
        "sadness": None,
        "dominant_emotion": None,
        "error": "service_unavailable",
    }
