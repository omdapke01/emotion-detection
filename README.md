# Emotion Detection App

This project is a Flask-based web application that analyzes customer feedback
text and detects emotions using the Watson NLP emotion classification endpoint.

## Features

- Emotion detection package for customer feedback text
- Flask web interface and HTTP endpoint
- Error handling for empty or invalid input
- Unit tests with `pytest`
- Static code analysis with `pylint`

## Local setup

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python server.py
```

Open `http://127.0.0.1:5000`.

## Test and lint

```bash
pytest
pylint EmotionDetection server.py
```
