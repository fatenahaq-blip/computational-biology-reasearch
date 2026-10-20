"""Stage 5: independent-cohort lung tumor vs normal MICROARRAY study.

GSE10072 -> train; GSE7670 -> external test.
These are microarrays (GPL96), NOT RNA-Seq.
No model selection or threshold tuning using the external cohort.
"""
import gzip
import io
import json
import re
import urllib.request
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, balanced_accuracy_score, confusion_matrix, f1_score, roc_auc_score
from sklearn.model_selection import GroupKFold, cross_validate
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

BASE = Path(__file__).resolve().parent
URLS = {
    "GSE10072": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE10nnn/GSE10072/matrix/GSE10072_series_matrix.txt.gz",
    "GSE7670": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE7nnn/GSE7670/matrix/GSE7670_series_matrix.txt.gz",
}

def parse_geo_matrix(accession):
    request = urllib.request.Request(URLS[accession], headers={"User-Agent": "academic-research-script/1.0"})
    with urllib.request.urlopen(request, timeout=180) as response:
        raw = gzip.decompress(response.read()).decode("utf-8")
    titles = ids = None
    table = []
    inside = False
    for line in raw.splitlines():
        if line.startswith("!Sample_title\t"):
            titles = [x.strip('"') for x in line.split("\t")[1:]]
        elif line.startswith("!Sample_geo_accession\t"):
            ids = [x.strip('"') for x in line.split("\t")[1:]]
        elif line.startswith("!series_matrix_table_begin"):
            inside = True
        elif line.startswith("!series_matrix_table_end"):
            inside = False
        elif inside:
            table.append(line)
    if not titles or not ids or len(titles) != len(ids) or not table:
        raise ValueError(f"Invalid GEO series matrix metadata: {accession}")
    matrix = pd.read_csv(io.StringIO("\n".join(table)), sep="\t", index_col=0)
    if matrix.shape[1] != len(ids):
        raise ValueError("Expression sample count does not match metadata")
    matrix.columns = ids
    if matrix.index.has_duplicates or matrix.columns.has_duplicates:
        raise ValueError("Duplicate probe or sample IDs")
    return matrix, list(zip(ids, titles))

def label_and_group(accession, sample_id, title):
    if accession == "GSE10072":
        match = re.match(r"^(Lung Tumor|Normal Lung)_GT(\d+)$", title, flags=re.I)
        if match is None:
            return None
        return (1 if match.group(1).lower() == "lung tumor" else 0, "GT" + match.group(2))
    if accession == "GSE7670":
        # Only numbered surgical patient tissue pairs; exclude mixtures, commercial tissue, and cell lines.
        match = re.match(r"^(\d+)([NT]):\s*(.*)$", title, flags=re.I)
        if match is None or "adenocarcinoma" not in match.group(3).lower():
            return None
        return (1 if match.group(2).upper() == "T" else 0, "PAT" + match.group(1))
    raise ValueError(accession)

def prepare(accession):
    matrix, metadata = parse_geo_matrix(accession)
    included = [(sid, *v) for sid, title in metadata if (v := label_and_group(accession, sid, title)) is not None]
    if not included:
        raise ValueError("No patient samples after filtering")
    ids = [v[0] for v in included]
    y = np.array([v[1] for v in included])
    groups = np.array([v[2] for v in included])
    x = matrix[ids].apply(pd.to_numeric, errors="raise").T
    if not np.isfinite(x.to_numpy()).all():
        raise ValueError("Nonfinite expression values")
    if set(y) != {0, 1}:
        raise ValueError("Both classes required")
    return x, y, groups

def run():
    train, y, groups = prepare("GSE10072")
    external, y_ext, ext_groups = prepare("GSE7670")
    shared = train.columns.intersection(external.columns, sort=False)
    shared = shared[~shared.str.startswith("AFFX-", na=False)]
    if len(shared) < 10000:
        raise ValueError(f"Insufficient shared GPL96 probes: {len(shared)}")
    X = train.loc[:, shared].to_numpy()
    Z = external.loc[:, shared].to_numpy()
    # Dataset preprocessing is intentionally not pooled across studies.
    # Note: RMA (GSE10072) versus MAS5 (GSE7670) may cause substantial domain shift.
    pipeline = make_pipeline(
        SelectKBest(f_classif, k=200),
        StandardScaler(),
        LogisticRegression(max_iter=3000, random_state=42)
    )
    cv = GroupKFold(n_splits=5)
    scores = cross_validate(pipeline, X, y, groups=groups, cv=cv,
                            scoring={"balanced_accuracy": "balanced_accuracy", "roc_auc": "roc_auc"})
    pipeline.fit(X, y)
    probabilities = pipeline.predict_proba(Z)[:, 1]
    predictions = pipeline.predict(Z)
    result = {
        "study_type": "independent-cohort microarray tumor-vs-normal; not original RNA-Seq model validation",
        "training_accession": "GSE10072",
        "external_accession": "GSE7670",
        "platform": "GPL96",
        "n_training_samples": len(y),
        "n_external_patient_samples": len(y_ext),
        "n_training_patient_groups": len(set(groups)),
        "n_external_patient_groups": len(set(ext_groups)),
        "training_class_counts": {"normal": int(sum(y == 0)), "tumor": int(sum(y == 1))},
        "external_class_counts": {"normal": int(sum(y_ext == 0)), "tumor": int(sum(y_ext == 1))},
        "shared_probes": len(shared),
        "train_group_cv_balanced_accuracy_mean": float(np.mean(scores["test_balanced_accuracy"])),
        "train_group_cv_roc_auc_mean": float(np.mean(scores["test_roc_auc"])),
        "external_accuracy": float(accuracy_score(y_ext, predictions)),
        "external_balanced_accuracy": float(balanced_accuracy_score(y_ext, predictions)),
        "external_f1": float(f1_score(y_ext, predictions)),
        "external_roc_auc": float(roc_auc_score(y_ext, probabilities)),
        "external_confusion_matrix": confusion_matrix(y_ext, predictions, labels=[0, 1]).tolist(),
        "caveats": [
            "Training uses RMA-normalized values; external uses MAS5-scaled values, with significant possible platform-processing shift.",
            "Matched patient tissue samples are grouped in cross-validation.",
            "External patient tissue data are not used for fitting or selecting hyperparameters.",
            "No verified gene symbols, biological biomarker claims or clinical utility are inferred.",
            "Exploratory study; patient metadata and study independence require further provenance review."
        ]
    }
    out = BASE / "results" / "cross_cohort_microarray.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    run()
