import pickle
import numpy as np
import sys
import warnings
warnings.filterwarnings("ignore")

from preprocess import preprocess_audio
from embeddings import get_embedding_chunked

with open("/Users/shreya/voice-health/models/classifier_v1.pkl", "rb") as f:
    pipeline = pickle.load(f)

def predict(audio_path):
    print(f"Loading audio: {audio_path}")
    waveform  = preprocess_audio(audio_path)

    print("Extracting features...")
    embedding = get_embedding_chunked(waveform).numpy().astype(np.float64)

    prediction = pipeline.predict(embedding)[0]
    probs      = pipeline.predict_proba(embedding)[0]

    print("\n=== Result ===")
    print(f"Prediction:         {'Depressed' if prediction == 1 else 'Not Depressed'}")
    print(f"Confidence:         {probs.max()*100:.1f}%")
    print(f"Depression prob:    {probs[1]*100:.1f}%")
    print(f"No depression prob: {probs[0]*100:.1f}%")

    return {
        "prediction": int(prediction),
        "label": "Depressed" if prediction == 1 else "Not Depressed",
        "depression_probability": round(float(probs[1]), 3),
        "confidence": round(float(probs.max()), 3)
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        audio_path = sys.argv[1]
    else:
        audio_path = "/Users/shreya/voice-health/data/raw/303.wav"

    predict(audio_path)
