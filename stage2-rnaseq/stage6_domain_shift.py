"""Stage 6: exploratory label-free normalization for cross-study microarray shift.

Training-only model selection; external labels used ONLY for final reporting.
Stage 5 external outcomes have already been observed: NOT a pristine test set.
"""
import json
from pathlib import Path
import numpy as np
from scipy.stats import rankdata, wasserstein_distance
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, balanced_accuracy_score, confusion_matrix, f1_score, roc_auc_score
from sklearn.model_selection import GroupKFold, cross_validate
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from cross_cohort_microarray import prepare

BASE = Path(__file__).resolve().parent

class SampleRepresentation(BaseEstimator, TransformerMixin):
    """Stateless transforms: no target cohort parameters are learned."""
    def __init__(self, method="raw"):
        self.method = method

    def fit(self, X, y=None):
        if self.method not in {"raw", "log2", "percentile_rank"}:
            raise ValueError("Unsupported representation")
        return self

    def transform(self, X):
        X = np.asarray(X, dtype=np.float64)
        if X.ndim != 2 or not np.isfinite(X).all():
            raise ValueError("Expected finite 2D expression matrix")
        if self.method == "raw":
            return X.copy()
        if self.method == "log2":
            # Clipping is fixed in advance, not tuned using external labels.
            return np.log2(np.maximum(X, 0.0) + 1.0)
        # Per-sample percentile ranks; no external sample labels or cohort stats.
        return np.vstack([rankdata(row, method="average") / len(row) for row in X])

def make_model(method, n_features=200):
    return Pipeline([
        ("representation", SampleRepresentation(method)),
        ("selection", SelectKBest(f_classif, k=n_features)),
        ("scale", StandardScaler()),
        ("classifier", LogisticRegression(max_iter=3000, random_state=42))
    ])

def experiment(train, y, groups, external, external_y):
    if not train.columns.equals(external.columns):
        raise ValueError("Feature identifiers/order must match")
    X, Z = train.to_numpy(), external.to_numpy()
    if not np.isfinite(X).all() or not np.isfinite(Z).all():
        raise ValueError("Nonfinite data")
    cv = GroupKFold(n_splits=5)
    methods = ["raw", "log2", "percentile_rank"]
    # All selection is on training data; external labels never enter CV.
    cv_results = {}
    for method in methods:
        scores = cross_validate(make_model(method), X, y, groups=groups, cv=cv,
            scoring={"balanced_accuracy": "balanced_accuracy", "roc_auc": "roc_auc"})
        cv_results[method] = {
            "balanced_accuracy_mean": float(scores["test_balanced_accuracy"].mean()),
            "balanced_accuracy_sd": float(scores["test_balanced_accuracy"].std()),
            "roc_auc_mean": float(scores["test_roc_auc"].mean())
        }
    # Tie-break order is pre-specified and favors the original method.
    winner = max(methods, key=lambda m: cv_results[m]["balanced_accuracy_mean"])
    external_results = {}
    for method in methods:
        model = make_model(method)
        model.fit(X, y)
        pred = model.predict(Z)
        proba = model.predict_proba(Z)[:, 1]
        external_results[method] = {
            "accuracy": float(accuracy_score(external_y, pred)),
            "balanced_accuracy": float(balanced_accuracy_score(external_y, pred)),
            "f1": float(f1_score(external_y, pred, zero_division=0)),
            "roc_auc": float(roc_auc_score(external_y, proba)),
            "tumor_sensitivity": float(np.mean(pred[external_y == 1] == 1)),
            "normal_specificity": float(np.mean(pred[external_y == 0] == 0)),
            "confusion_matrix": confusion_matrix(external_y, pred, labels=[0, 1]).tolist()
        }
    # Label-free descriptive shift only, calculated on the aligned matrices.
    shift = {}
    for method in methods:
        transformer = SampleRepresentation(method)
        A, B = transformer.transform(X), transformer.transform(Z)
        shift[method] = {
            "train_median": float(np.median(A)),
            "external_median": float(np.median(B)),
            "pooled_value_wasserstein": float(wasserstein_distance(
                A.ravel()[::max(1, A.size // 50000)],
                B.ravel()[::max(1, B.size // 50000)]))
        }
    return {
        "study_type": "exploratory post-hoc normalization sensitivity analysis",
        "training_samples": len(y),
        "external_samples": len(external_y),
        "aligned_probes": X.shape[1],
        "selection_rule": "maximum grouped-CV balanced accuracy on training cohort only; ties favor raw",
        "selected_method": winner,
        "training_cv": cv_results,
        "external_results_all_methods": external_results,
        "label_free_distribution_diagnostics": shift,
        "integrity_notes": [
            "No external labels used in fitting, feature selection or method choice.",
            "External labels were previously inspected in Stage 5; this is exploratory, not untouched validation.",
            "Per-sample ranks remove absolute expression scale and may erase biological signal.",
            "Pooled-value distribution differences do not establish correction of biological batch effects.",
            "Any improvement requires a new independent cohort for confirmation."
        ]
    }

def main():
    train, y, groups = prepare("GSE10072")
    external, external_y, _ = prepare("GSE7670")
    shared = train.columns.intersection(external.columns, sort=False)
    shared = shared[~shared.str.startswith("AFFX-", na=False)]
    if len(shared) < 10000:
        raise ValueError("Insufficient shared probes")
    train, external = train.loc[:, shared], external.loc[:, shared]
    results = experiment(train, y, groups, external, external_y)
    path = BASE / "results" / "stage6_domain_shift.json"
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()
