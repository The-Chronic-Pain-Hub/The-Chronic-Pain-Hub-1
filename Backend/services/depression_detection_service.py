"""
Depression Detection Service using wav2vec2 model
Adapted from api.py for integration into main Backend
"""
import torch
import numpy as np
import pickle
import os
from transformers import Wav2Vec2Processor, Wav2Vec2Model
import torchaudio

# Load wav2vec2 model for embedding extraction
processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h")
wav2vec_model = Wav2Vec2Model.from_pretrained("facebook/wav2vec2-base-960h")

# Load trained classifier
# Path: Backend/services/ -> Backend/ -> project_root/models/
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
CLASSIFIER_PATH = os.path.join(project_root, "models", "classifier_v1.pkl")

if not os.path.exists(CLASSIFIER_PATH):
    raise FileNotFoundError(f"Classifier model not found at {CLASSIFIER_PATH}")

with open(CLASSIFIER_PATH, "rb") as f:
    classifier_pipeline = pickle.load(f)

print(f"[Depression Detection] Loaded classifier from {CLASSIFIER_PATH}")

# Audio preprocessing
def preprocess_audio(file_path, target_sample_rate=16000):
    """Convert audio to 16kHz mono waveform"""
    waveform, sample_rate = torchaudio.load(file_path)
    if waveform.shape[0] > 1:
        waveform = waveform.mean(dim=0, keepdim=True)
    if sample_rate != target_sample_rate:
        resampler = torchaudio.transforms.Resample(sample_rate, target_sample_rate)
        waveform = resampler(waveform)
    return waveform.squeeze()


def get_embedding_chunked(waveform):
    """Extract wav2vec2 embeddings from audio waveform"""
    CHUNK_SECONDS = 30
    SAMPLE_RATE = 16000
    CHUNK_SIZE = CHUNK_SECONDS * SAMPLE_RATE
    
    chunks = waveform.split(CHUNK_SIZE)
    chunk_embeddings = []
    
    for chunk in chunks:
        if len(chunk) < SAMPLE_RATE:
            continue
        inputs = processor(
            chunk.numpy(),
            sampling_rate=SAMPLE_RATE,
            return_tensors="pt",
            padding=True
        )
        with torch.no_grad():
            outputs = wav2vec_model(**inputs)
        emb = outputs.last_hidden_state.mean(dim=1)
        chunk_embeddings.append(emb)
    
    return torch.stack(chunk_embeddings).mean(dim=0)


def analyze_depression_from_audio(audio_path: str) -> dict:
    """
    Analyze audio file for depression indicators using wav2vec2 classifier
    
    Args:
        audio_path: Path to audio file
    
    Returns:
        Dictionary with prediction, probabilities, and confidence
    """
    try:
        # Preprocess audio
        waveform = preprocess_audio(audio_path)
        
        # Extract embeddings
        embedding = get_embedding_chunked(waveform).numpy().astype(np.float64)
        
        # Predict
        prediction = classifier_pipeline.predict(embedding)[0]
        probabilities = classifier_pipeline.predict_proba(embedding)[0]
        
        return {
            "prediction": int(prediction),
            "label": "Depressed" if prediction == 1 else "Not Depressed",
            "depression_probability": round(float(probabilities[1]), 3),
            "no_depression_probability": round(float(probabilities[0]), 3),
            "confidence": round(float(probabilities.max()), 3),
        }
    except Exception as e:
        raise Exception(f"Depression analysis failed: {str(e)}")
