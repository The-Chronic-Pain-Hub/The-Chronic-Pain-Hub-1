import numpy as np
import pandas as pd

# Load all processed IDs
all_ids = np.load("/Users/shreya/voice-health/features/processed_ids.npy")
print(f"Total processed IDs: {len(all_ids)}")

# Load train CSV
train = pd.read_csv("/Users/shreya/voice-health/DAIC-WOZ/train_split_Depression_AVEC2017.csv")

# Match labels to IDs in the same order
df = train[train["Participant_ID"].isin(all_ids)]
df = df.set_index("Participant_ID").reindex(all_ids)

# Check for any IDs that didn't get a label
missing = df[df["PHQ8_Binary"].isna()]
if len(missing) > 0:
    print(f"Warning: {len(missing)} IDs had no label match:", missing.index.tolist())

df = df.dropna(subset=["PHQ8_Binary"])

np.save("/Users/shreya/voice-health/features/labels.npy", df["PHQ8_Binary"].values.astype(int))
np.save("/Users/shreya/voice-health/features/participant_ids.npy", df.index.values)

print(f"Saved {len(df)} labels")
print(f"Depressed:     {df['PHQ8_Binary'].sum()}")
print(f"Not depressed: {(df['PHQ8_Binary']==0).sum()}")
