from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pickle
import numpy as np
import tempfile
import os
import warnings
warnings.filterwarnings("ignore")

import sys
sys.path.append(os.path.dirname(__file__))
from preprocess import preprocess_audio
from embeddings import get_embedding_chunked

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_PATH = "/Users/shreya/voice-health/models/classifier_v1.pkl"
with open(MODEL_PATH, "rb") as f:
    pipeline = pickle.load(f)

@app.get("/")
def root():
    return {"status": "Voice Health API is running"}

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    suffix = os.path.splitext(file.filename)[1] or ".wav"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name
    try:
        # Convert to wav if needed (handles webm/ogg from browser)
        from pydub import AudioSegment
        converted_path = tmp_path + "_converted.wav"
        audio = AudioSegment.from_file(tmp_path)
        audio.export(converted_path, format="wav")
        waveform  = preprocess_audio(converted_path)
        embedding = get_embedding_chunked(waveform).numpy().astype(np.float64)
        pred      = pipeline.predict(embedding)[0]
        probs     = pipeline.predict_proba(embedding)[0]
        os.unlink(converted_path)
        return {
            "prediction":                int(pred),
            "label":                     "Depressed" if pred == 1 else "Not Depressed",
            "depression_probability":    round(float(probs[1]), 3),
            "no_depression_probability": round(float(probs[0]), 3),
            "confidence":                round(float(probs.max()), 3),
        }
    except Exception as e:
        return {"error": str(e)}
    finally:
        os.unlink(tmp_path)