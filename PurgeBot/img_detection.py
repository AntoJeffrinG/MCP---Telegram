import requests
import json
from config import SIGHTENGINE_API_USER, SIGHTENGINE_API_SECRET

SIGHTENGINE_URL = "https://api.sightengine.com/1.0/check.json"

def is_abusive_image(image_path: str) -> bool:
    """Check if an image contains abusive content using SightEngine API."""
    params = {
        "models": "nudity-2.1,weapon,alcohol,recreational_drug,medical,offensive-2.0,text-content,gore-2.0,tobacco,violence,self-harm",
        "api_user": SIGHTENGINE_API_USER,
        "api_secret": SIGHTENGINE_API_SECRET
    }

    with open(image_path, "rb") as image_file:
        files = {"media": image_file}
        response = requests.post(SIGHTENGINE_URL, files=files, data=params)

    if response.status_code == 200:
        output = response.json()
        
        # Extract and check relevant categories
        if (
            output.get("nudity", {}).get("raw", 0) > 0.8 or  
            output.get("offensive", {}).get("prob", 0) > 0.8 or  
            output.get("violence", {}).get("prob", 0) > 0.8 or  
            output.get("gore", {}).get("prob", 0) > 0.8  
        ):
            return True  # Image contains abusive content

    return False  # Image is safe
