"""Stage 3: repeated CV and RNA-Seq feature stability (research, not clinical)."""
import json
from pathlib import Path
import numpy as np
from sklearn.dummy import DummyClassifier
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import RepeatedStratifiedKFold, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder, StandardScaler
from rnaseq_analysis import load_uci_rnaseq

SEED = 42

def validate_stability(X, labels, n_features=500, n_splits=5, n_repeats=3):
    X = np.asarray(X, dtype=float)
    labels = np.asarray(labels).ravel()
    if X.ndim != 2 or X.shape[0] != len(labels) or not np.isfinite(X).all():
        raise ValueError("Invalid data")
    y = LabelEncoder().fit_transform(labels)
    if np.bincount(y).min() < 10:
        raise ValueError("At least 10 samples per class required")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=SEED
    )
    k = min(n_features, X.shape[1])
    splitter = RepeatedStratifiedKFold(n_splits=n_splits, n_repeats=n_repeats, random_state=SEED)
    scores, baseline_scores, selected_sets = [], [], []
    for train_idx, val_idx in splitter.split(X_train, y_train):
        model = Pipeline([
            ("select", SelectKBest(f_classif, k=k)),
            ("scale", StandardScaler()),
            ("classifier", LogisticRegression(max_iter=3000, class_weight="balanced", random_state=SEED))
        ])
        model.fit(X_train[train_idx], y_train[train_idx])
        pred = model.predict(X_train[val_idx])
        scores.append(f1_score(y_train[val_idx], pred, average="macro"))
        selected_sets.append(set(model.named_steps["select"].get_support(indices=True).tolist()))
        baseline = DummyClassifier(strategy="most_frequent")
        baseline.fit(X_train[train_idx], y_train[train_idx])
        baseline_scores.append(f1_score(y_train[val_idx], baseline.predict(X_train[val_idx]), average="macro", zero_division=0))
    # Pairwise Jaccard similarity over all CV fits; descriptive, not an inferential CI.
    jaccards = []
    for i in range(len(selected_sets)):
        for j in range(i + 1, len(selected_sets)):
            a, b = selected_sets[i], selected_sets[j]
            jaccards.append(len(a & b) / len(a | b))
    counts = np.bincount([i for s in selected_sets for i in s], minlength=X.shape[1])
    stable = np.flatnonzero(counts == len(selected_sets))
    # Fit once on the fixed training split; bootstrap the untouched test predictions.
    final_model = Pipeline([
        ("select", SelectKBest(f_classif, k=k)),
        ("scale", StandardScaler()),
        ("classifier", LogisticRegression(max_iter=3000, class_weight="balanced", random_state=SEED))
    ])
    final_model.fit(X_train, y_train)
    test_pred = final_model.predict(X_test)
    rng = np.random.default_rng(SEED)
    boot_acc = []
    for _ in range(2000):
        idx = rng.integers(0, len(y_test), len(y_test))
        boot_acc.append(accuracy_score(y_test[idx], test_pred[idx]))
    return {
        "n_samples": int(X.shape[0]), "n_features_total": int(X.shape[1]),
        "train_samples": int(len(y_train)), "test_samples": int(len(y_test)),
        "n_features_selected_per_fit": int(k),
        "cv_folds": int(n_splits), "cv_repeats": int(n_repeats),
        "cv_macro_f1_mean": float(np.mean(scores)),
        "cv_macro_f1_sd_across_folds": float(np.std(scores)),
        "baseline_macro_f1_mean": float(np.mean(baseline_scores)),
        "mean_pairwise_feature_jaccard": float(np.mean(jaccards)),
        "features_selected_in_all_fits": int(len(stable)),
        "stable_anonymous_feature_indices": stable.tolist(),
        "test_accuracy": float(accuracy_score(y_test, test_pred)),
        "test_macro_f1": float(f1_score(y_test, test_pred, average="macro")),
        "test_accuracy_bootstrap_percentile_95": [float(v) for v in np.quantile(boot_acc, [0.025, 0.975])],
        "bootstrap_note": "Percentile interval conditional on fixed fitted model and held-out test sample; does not quantify external generalization."
    }

if __name__ == "__main__":
    X, labels = load_uci_rnaseq()
    result = validate_stability(X, labels)
    target = Path(__file__).resolve().parent / "results" / "stage3_stability.json"
    target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k != "stable_anonymous_feature_indices"}, indent=2))
