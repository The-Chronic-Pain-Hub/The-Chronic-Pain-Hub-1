import pickle
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings("ignore")
import os
from preprocess import preprocess_audio
from embeddings import get_embedding_chunked

with open("/Users/shreya/voice-health/models/classifier_v1.pkl", "rb") as f:
    pipeline = pickle.load(f)

train = pd.read_csv("/Users/shreya/voice-health/DAIC-WOZ/train_split_Depression_AVEC2017.csv")

# Test on 10 participants — 5 depressed, 5 not
depressed     = train[train["PHQ8_Binary"] == 1]["Participant_ID"].tolist()[-5:]
not_depressed = train[train["PHQ8_Binary"] == 0]["Participant_ID"].tolist()[-5:]
test_ids      = depressed + not_depressed

print(f"{'ID':<8} {'Actual':<16} {'Predicted':<16} {'Confidence':<12} {'Correct'}")
print("-" * 65)

correct = 0
for pid in test_ids:
    path = f"/Users/shreya/voice-health/data/raw/{pid}.wav"
    if not os.path.exists(path):
        print(f"{pid:<8} file not found, skipping")
        continue

    actual_label = train[train["Participant_ID"] == pid]["PHQ8_Binary"].values[0]
    actual_str   = "Depressed" if actual_label == 1 else "Not Depressed"

    waveform  = preprocess_audio(path)
    embedding = get_embedding_chunked(waveform).numpy().astype(np.float64)
    pred      = pipeline.predict(embedding)[0]
    conf      = pipeline.predict_proba(embedding)[0].max()
    pred_str  = "Depressed" if pred == 1 else "Not Depressed"
    is_correct = "✓" if pred == actual_label else "✗"
    if pred == actual_label:
        correct += 1

    print(f"{pid:<8} {actual_str:<16} {pred_str:<16} {conf*100:<11.1f}% {is_correct}")

print("-" * 65)
print(f"Accuracy on this batch: {correct}/{len(test_ids)} ({correct/len(test_ids)*100:.0f}%)")
