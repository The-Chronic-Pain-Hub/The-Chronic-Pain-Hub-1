import pandas as pd

train = pd.read_csv("train_split_Depression_AVEC2017.csv")

depressed     = train[train["PHQ8_Binary"] == 1]["Participant_ID"].tolist()
not_depressed = train[train["PHQ8_Binary"] == 0]["Participant_ID"].head(30).tolist()

starter = depressed + not_depressed
starter.sort()

print("Download these zips:")
for pid in starter:
    print(f"  {pid}_P.zip")

print(f"\nTotal to download: {len(starter)} files")
