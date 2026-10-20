"""Stage 8 patient-level independence audit for GSE31547.

Recreates locked predictions without modifying Stage 7 classifier.
Cluster-bootstrap intervals resample title-inferred patient groups.
"""
import json
from collections import Counter, defaultdict
from pathlib import Path
import numpy as np
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import balanced_accuracy_score, confusion_matrix
from cross_cohort_microarray import prepare
from stage6_domain_shift import SampleRepresentation
from stage7_third_cohort import load_third_cohort

BASE = Path(__file__).resolve().parent

def cluster_bootstrap(y, pred, groups, n_boot=4000, seed=42):
    y = np.asarray(y)
    pred = np.asarray(pred)
    groups = np.asarray(groups)
    unique = np.unique(groups)
    rng = np.random.default_rng(seed)
    estimates = []
    for _ in range(n_boot):
        drawn = rng.choice(unique, len(unique), replace=True)
        idx = np.concatenate([np.flatnonzero(groups == g) for g in drawn])
        if len(np.unique(y[idx])) < 2:
            continue
        estimates.append(balanced_accuracy_score(y[idx], pred[idx]))
    if len(estimates) < n_boot * 0.9:
        raise ValueError("Insufficient bootstrap resamples with both classes")
    return [float(x) for x in np.quantile(estimates, [0.025, 0.975])], len(estimates)

def audit():
    train, train_y, train_groups = prepare("GSE10072")
    third, y, ids = load_third_cohort()
    shared = train.columns.intersection(third.columns, sort=False)
    shared = shared[~shared.str.startswith("AFFX-", na=False)]
    X, Z = train.loc[:, shared].to_numpy(), third.loc[:, shared].to_numpy()
    model = Pipeline([
        ("representation", SampleRepresentation("percentile_rank")),
        ("selection", SelectKBest(f_classif, k=200)),
        ("scale", StandardScaler()),
        ("classifier", LogisticRegression(max_iter=3000, random_state=42))
    ])
    model.fit(X, train_y)
    pred = model.predict(Z)
    cm = confusion_matrix(y, pred, labels=[0, 1]).tolist()
    if cm != [[19, 1], [0, 30]]:
        raise ValueError(f"Stage 7 prediction mismatch: {cm}")
    by_patient = defaultdict(list)
    for i, group in enumerate(ids):
        by_patient[str(group)].append(i)
    repeated = {k: len(v) for k, v in by_patient.items() if len(v) > 1}
    mixed_label_groups = sorted(k for k, v in by_patient.items() if len(set(y[v])) > 1)
    patient_outcome = []
    for k, indices in sorted(by_patient.items()):
        patient_outcome.append({
            "title_patient_id": k,
            "n_specimens": len(indices),
            "n_normal": int(np.sum(y[indices] == 0)),
            "n_tumor": int(np.sum(y[indices] == 1)),
            "n_errors": int(np.sum(y[indices] != pred[indices]))
        })
    ci, accepted = cluster_bootstrap(y, pred, ids)
    return {
        "source": "GSE31547 GEO sample titles (title-derived patient IDs; clinical identity unverified)",
        "n_specimens": len(ids),
        "n_unique_title_patient_ids": len(by_patient),
        "n_repeated_title_patient_ids": len(repeated),
        "repeated_id_counts": repeated,
        "mixed_tumor_normal_title_groups": mixed_label_groups,
        "n_mixed_groups": len(mixed_label_groups),
        "train_patient_groups": len(set(train_groups)),
        "external_specimen_balanced_accuracy": float(balanced_accuracy_score(y, pred)),
        "external_confusion_matrix": cm,
        "patient_cluster_bootstrap_balanced_accuracy_95": ci,
        "cluster_bootstrap_valid_replicates": accepted,
        "per_title_group_summary": patient_outcome,
        "limitations": [
            "Title-inferred identifiers may not represent unique biological patients; verify original clinical metadata.",
            "Cluster bootstrap accounts for repeated specimens within inferred groups but not study selection bias.",
            "The original Stage 7 model and 0.5 threshold were not changed.",
            "Results are microarray-based, not RNA-Seq; no clinical diagnosis or biomarker validation."
        ]
    }

if __name__ == "__main__":
    result = audit()
    path = BASE / "results" / "stage8_patient_independence_audit.json"
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k != "per_title_group_summary"}, indent=2))
