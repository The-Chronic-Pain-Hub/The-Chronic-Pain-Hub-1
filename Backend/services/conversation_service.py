import os
from openai import OpenAI
from dotenv import load_dotenv
import json
from typing import List, Dict

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

PLACEHOLDER_IMAGES = {
    "sharp": "/images/sharp.gif",
    "dull": "/images/dull.jpg",
    "burning": "/images/burning.gif",
    "tingling": "/images/Tingling.jpg", 
    "throbbing": "/images/throbbing.jpg",
    "radiating": "/images/radiating.gif",
    "pulsing": "/images/pulsing.gif",
    "pounding": "/images/pounding.gif"
}

def generateFollowUpQuestions(converHistory: List[Dict]) -> dict:
    """Generate visual pain assessment question using available GIF animations"""
    
    # Fixed question using available GIFs
    result = {
        "question": "Which image best describes your pain sensation?",
        "question_type": "quality",
        "options": [
            {
                "id": "A",
                "text": "Sharp, stabbing pain",
                "image_key": "sharp",
                "image_url": "/images/sharp.gif"
            },
            {
                "id": "B", 
                "text": "Pulsing, throbbing pain",
                "image_key": "pulsing",
                "image_url": "/images/pulsing.gif"
            },
            {
                "id": "C",
                "text": "Burning, hot sensation", 
                "image_key": "burning",
                "image_url": "/images/burning.gif"
            }
        ],
        "round_number": 1
    }
    
    return result
            