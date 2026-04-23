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
    """Generate bilingual visual pain assessment question using available GIF animations"""
    
    # Fixed bilingual question using available GIFs
    result = {
        "question": "Which image best describes your pain sensation? | 哪个图像最能描述您的疼痛感觉？",
        "question_type": "quality",
        "options": [
            {
                "id": "A",
                "text": "Sharp, stabbing pain | 尖锐刺痛感",
                "image_key": "sharp",
                "image_url": "/images/sharp.gif"
            },
            {
                "id": "B", 
                "text": "Pulsing, throbbing pain | 搏动性疼痛",
                "image_key": "pulsing",
                "image_url": "/images/pulsing.gif"
            },
            {
                "id": "C",
                "text": "Burning, hot sensation | 灼烧样疼痛", 
                "image_key": "burning",
                "image_url": "/images/burning.gif"
            }
        ],
        "round_number": 1
    }
    
    return result
            