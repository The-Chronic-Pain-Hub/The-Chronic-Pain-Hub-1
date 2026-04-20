import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline
import pickle
import warnings
warnings.filterwarnings("ignore")

X = np.load("/Users/shreya/voice-health/features/embeddings.npy").squeeze().astype(np.float64)
y = np.load("/Users/shreya/voice-health/features/labels.npy")

print(f"Training on {len(X)} participants")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("pca",    PCA(n_components=30)),
    ("clf",    LogisticRegression(max_iter=1000, class_weight="balanced"))
])

pipeline.fit(X_train, y_train)

preds = pipeline.predict(X_test)
probs = pipeline.predict_proba(X_test)[:, 1]

print("\n=== Results ===")
print(classification_report(y_test, preds, target_names=["Not Depressed", "Depressed"]))
print(f"AUC-ROC: {roc_auc_score(y_test, probs):.3f}")

print("\n=== Confusion Matrix ===")
cm = confusion_matrix(y_test, preds)
print(f"True Negatives:  {cm[0][0]}  (correctly said not depressed)")
print(f"False Positives: {cm[0][1]}  (wrongly flagged as depressed)")
print(f"False Negatives: {cm[1][0]}  (missed depressed people)")
print(f"True Positives:  {cm[1][1]}  (correctly caught depressed)")

with open("/Users/shreya/voice-health/models/classifier_v1.pkl", "wb") as f:
    pickle.dump(pipeline, f)
print("\nModel saved.")
