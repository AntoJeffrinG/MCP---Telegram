import requests
import json
from config import PERSPECTIVE_API_KEY

PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

def is_toxic(message: str) -> bool:
    """Check if a message is toxic using Google's Perspective API."""
    payload = {
        "comment": {"text": message},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}}
    }

    params = {"key": PERSPECTIVE_API_KEY}
    response = requests.post(PERSPECTIVE_API_URL, params=params, json=payload)

    if response.status_code == 200:
        result = response.json()
        toxicity_score = result["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
        return toxicity_score > 0.8  # Flag as toxic if confidence is high
    else:
        print("Error:", response.json())
        return False  # Default to non-toxic if API fails this code has a system to detect text abuse. Can you add image, video and audio abusive content detection too in this