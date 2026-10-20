"""Stage 7: locked, third-cohort test of percentile-rank lung microarray classifier.

Protocol: STAGE7_LOCKED_PROTOCOL.md committed before outcome evaluation.
Train GSE10072; evaluate once on previously unused GSE31547.
"""
import json
import re
from pathlib import Path
import numpy as np
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import balanced_accuracy_score, confusion_matrix, f1_score, roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from cross_cohort_microarray import parse_geo_matrix, prepare
from stage6_domain_shift import SampleRepresentation

BASE = Path(__file__).resolve().parent
GSE31547_URL = (
    "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE31nnn/"
    "GSE31547/matrix/GSE31547_series_matrix.txt.gz"
)

def parse_locked_title(title):
    """Only GEO-verified 30 tumor L(A) and 20 normal NL(A) sample title forms."""
    match = re.fullmatch(r"(\d+)(NL|L)\(A\)", title.strip(), flags=re.I)
    if match is None:
        raise ValueError(f"Unexpected third-cohort sample title: {title!r}")
    return (0 if match.group(2).upper() == "NL" else 1, match.group(1))

def load_third_cohort():
    # parse_geo_matrix is a metadata-and-matrix reader only, not a model fitting step.
    # Temporarily register a verified GEO matrix URL for this new accession.
    from cross_cohort_microarray import URLS
    URLS["GSE31547"] = GSE31547_URL
    matrix, metadata = parse_geo_matrix("GSE31547")
    if len(metadata) != 50:
        raise ValueError(f"Expected exactly 50 GSE31547 samples, got {len(metadata)}")
    parsed = [(sid, *parse_locked_title(title)) for sid, title in metadata]
    labels = np.asarray([p[1] for p in parsed], dtype=int)
    if (int(sum(labels == 0)), int(sum(labels == 1))) != (20, 30):
        raise ValueError("GSE31547 class composition differs from registered protocol")
    ids = [p[0] for p in parsed]
    data = matrix.loc[:, ids].apply(lambda c: c.astype(float)).T
    if not np.isfinite(data.to_numpy()).all():
        raise ValueError("Nonfinite GSE31547 expression values")
    return data, labels, [p[2] for p in parsed]

def wilson_interval(successes, total, z=1.959963984540054):
    if total <= 0:
        raise ValueError("No samples")
    p = successes / total
    den = 1 + z * z / total
    mid = (p + z * z / (2 * total)) / den
    half = z * np.sqrt(p * (1 - p) / total + z * z / (4 * total * total)) / den
    return [float(max(0, mid - half)), float(min(1, mid + half))]

def evaluate_locked(train, train_y, third, third_y, third_patient_ids):
    if not train.columns.is_unique or not third.columns.is_unique:
        raise ValueError("Nonunique probe identifiers")
    shared = train.columns.intersection(third.columns, sort=False)
    shared = shared[~shared.str.startswith("AFFX-", na=False)]
    if len(shared) < 10000:
        raise ValueError("Too few shared GPL96 probe identifiers")
    X, Z = train.loc[:, shared].to_numpy(), third.loc[:, shared].to_numpy()
    if not np.isfinite(X).all() or not np.isfinite(Z).all():
        raise ValueError("Nonfinite expression values")
    model = Pipeline([
        ("representation", SampleRepresentation("percentile_rank")),
        ("selection", SelectKBest(f_classif, k=200)),
        ("scale", StandardScaler()),
        ("classifier", LogisticRegression(max_iter=3000, random_state=42))
    ])
    model.fit(X, train_y)
    probabilities = model.predict_proba(Z)[:, 1]
    predicted = model.predict(Z)
    cm = confusion_matrix(third_y, predicted, labels=[0, 1])
    tn, fp, fn, tp = [int(x) for x in cm.ravel()]
    return {
        "protocol": "STAGE7_LOCKED_PROTOCOL.md",
        "training_accession": "GSE10072",
        "held_out_accession": "GSE31547",
        "platform": "GPL96 microarray (not RNA-Seq)",
        "training_samples": int(len(train_y)),
        "held_out_samples": int(len(third_y)),
        "held_out_unique_patient_title_ids": len(set(third_patient_ids)),
        "shared_probe_ids": int(len(shared)),
        "selected_probe_count": 200,
        "representation": "within-sample percentile_rank",
        "threshold": 0.5,
        "balanced_accuracy": float(balanced_accuracy_score(third_y, predicted)),
        "macro_f1": float(f1_score(third_y, predicted, average="macro")),
        "roc_auc": float(roc_auc_score(third_y, probabilities)),
        "tumor_sensitivity": tp / (tp + fn),
        "normal_specificity": tn / (tn + fp),
        "tumor_sensitivity_wilson_95": wilson_interval(tp, tp + fn),
        "normal_specificity_wilson_95": wilson_interval(tn, tn + fp),
        "confusion_matrix": cm.tolist(),
        "notes": [
            "Third-cohort labels used only for locked final evaluation.",
            "No model fitting, threshold tuning or feature selection on third cohort.",
            "Wilson intervals treat specimens as independent; verify patient-level metadata before inferential interpretation.",
            "No biomarker or clinical utility claims."
        ]
    }

def main():
    train, y, _ = prepare("GSE10072")
    third, y_third, patient_ids = load_third_cohort()
    result = evaluate_locked(train, y, third, y_third, patient_ids)
    out = BASE / "results" / "stage7_third_cohort.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
