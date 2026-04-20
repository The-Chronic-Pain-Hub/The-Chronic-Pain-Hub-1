import os
import shutil
import pandas as pd
import numpy as np

daic_root  = "/Users/shreya/voice-health/DAIC-WOZ"
output_dir = "/Users/shreya/voice-health/data/raw"
os.makedirs(output_dir, exist_ok=True)

copied = []
for fname in os.listdir(daic_root):
    if fname.endswith("_AUDIO.wav"):
        participant_id = fname.replace("_AUDIO.wav", "")
        src = os.path.join(daic_root, fname)
        dst = os.path.join(output_dir, f"{participant_id}.wav")
        shutil.copy(src, dst)
        copied.append(int(participant_id))
        print(f"Copied {participant_id}")

print(f"\nCopied {len(copied)} audio files")

train = pd.read_csv("/Users/shreya/voice-health/DAIC-WOZ/train_split_Depression_AVEC2017.csv")
df    = train[train["Participant_ID"].isin(copied)]
df    = df.sort_values("Participant_ID")

np.save("/Users/shreya/voice-health/features/labels.npy",          df["PHQ8_Binary"].values)
np.save("/Users/shreya/voice-health/features/participant_ids.npy", df["Participant_ID"].values)

print(f"\nSaved {len(df)} labels")
print(f"Depressed:     {df['PHQ8_Binary'].sum()}")
print(f"Not depressed: {(df['PHQ8_Binary']==0).sum()}")
