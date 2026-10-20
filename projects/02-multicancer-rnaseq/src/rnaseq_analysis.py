"""RNA-Seq tumor classification using UCI dataset 401 (CC BY 4.0)."""
import json
from pathlib import Path
import numpy as np
import io
import tarfile
import urllib.request
import zipfile
import pandas as pd

DATASET_URL = "https://archive.ics.uci.edu/static/public/401/gene+expression+cancer+rna+seq.zip"

def load_uci_rnaseq():
    """Load the original UCI RNA-Seq ZIP containing a nested TAR.GZ archive."""
    request = urllib.request.Request(DATASET_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(request, timeout=180) as response:
        zip_bytes = response.read()
    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as archive:
        tar_names = [n for n in archive.namelist() if n.endswith(".tar.gz")]
        if len(tar_names) != 1:
            raise ValueError("Expected one nested RNA-Seq TAR.GZ archive")
        with tarfile.open(fileobj=io.BytesIO(archive.read(tar_names[0])), mode="r:gz") as nested:
            names = nested.getnames()
            data_name = next(n for n in names if n.endswith("/data.csv"))
            label_name = next(n for n in names if n.endswith("/labels.csv"))
            with nested.extractfile(data_name) as f:
                data = pd.read_csv(f, index_col=0)
            with nested.extractfile(label_name) as f:
                labels = pd.read_csv(f, index_col=0)
    if data.shape != (801, 20531) or labels.shape[0] != 801:
        raise ValueError(f"Unexpected dataset dimensions: {data.shape}, {labels.shape}")
    if not data.index.equals(labels.index):
        labels = labels.reindex(data.index)
    if labels.isna().any().any():
        raise ValueError("Missing or unmatched cancer labels")
    return data.to_numpy(), labels.iloc[:, 0].to_numpy()

from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix
from sklearn.model_selection import StratifiedKFold, cross_validate, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder, StandardScaler

SEED = 42

def evaluate(X, labels, n_features=500):
    X = np.asarray(X, dtype=np.float64)
    labels = np.asarray(labels).ravel()
    if X.ndim != 2 or len(X) != len(labels) or not np.isfinite(X).all():
        raise ValueError("Invalid expression matrix or labels")
    encoder = LabelEncoder()
    y = encoder.fit_transform(labels)
    if np.bincount(y).min() < 8:
        raise ValueError("At least eight samples per class required")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=SEED
    )
    k = min(n_features, X.shape[1])
    pipeline = Pipeline([
        ("select", SelectKBest(f_classif, k=k)),
        ("scale", StandardScaler()),
        ("model", LogisticRegression(max_iter=3000, class_weight="balanced", random_state=SEED))
    ])
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)
    scores = cross_validate(pipeline, X_train, y_train, cv=cv,
                            scoring={"accuracy": "accuracy", "macro_f1": "f1_macro"})
    pipeline.fit(X_train, y_train)
    pred = pipeline.predict(X_test)
    return {
        "dataset_shape": list(X.shape),
        "classes": encoder.classes_.tolist(),
        "selected_features": k,
        "cv_accuracy_mean": float(scores["test_accuracy"].mean()),
        "cv_accuracy_std": float(scores["test_accuracy"].std()),
        "cv_macro_f1_mean": float(scores["test_macro_f1"].mean()),
        "test_accuracy": float(accuracy_score(y_test, pred)),
        "test_macro_f1": float(f1_score(y_test, pred, average="macro")),
        "confusion_matrix": confusion_matrix(y_test, pred).tolist(),
        "classification_report": classification_report(
            y_test, pred, target_names=encoder.classes_, output_dict=True, zero_division=0
        ),
        "selected_feature_indices": pipeline.named_steps["select"].get_support(indices=True).tolist()
    }

if __name__ == "__main__":
    X, y = load_uci_rnaseq()
    results = evaluate(X, y)
    out = Path("results/rnaseq_metrics.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print("Test accuracy:", results["test_accuracy"])
    print("Test macro F1:", results["test_macro_f1"])
