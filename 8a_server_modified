"""Flask web app for customer feedback emotion analytics."""

from __future__ import annotations

from flask import Flask, jsonify, render_template, request

from EmotionDetection import emotion_detector

app = Flask(__name__)


@app.get("/")
def index() -> str:
    """Render the main app page."""
    return render_template("index.html")


@app.get("/emotionDetector")
def detect_emotion():
    """Return a formatted emotion analysis response."""
    text_to_analyze = request.args.get("textToAnalyze", "")
    response = emotion_detector(text_to_analyze)

    if response["error"] == "invalid_text":
        return "Invalid text! Please try again!", 400
    if response["error"] == "service_unavailable":
        return (
            "Emotion service is temporarily unavailable. Please try again later.",
            503,
        )

    formatted_response = (
        "For the given statement, the system response is "
        f"'anger': {response['anger']}, "
        f"'disgust': {response['disgust']}, "
        f"'fear': {response['fear']}, "
        f"'joy': {response['joy']} and "
        f"'sadness': {response['sadness']}. "
        f"The dominant emotion is {response['dominant_emotion']}."
    )
    return formatted_response


@app.get("/api/health")
def health_check():
    """Return a small health response for local verification."""
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
