"""Educational breast cancer feature classification; not for clinical use."""
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import balanced_accuracy_score, roc_auc_score

SEED = 42


def run_experiment():
    dataset = load_breast_cancer()
    x_train, x_test, y_train, y_test = train_test_split(
        dataset.data, dataset.target, test_size=0.2,
        random_state=SEED, stratify=dataset.target
    )
    models = {
        "logistic_regression": make_pipeline(
            StandardScaler(), LogisticRegression(max_iter=2000, random_state=SEED)
        ),
        "random_forest": RandomForestClassifier(
            n_estimators=200, random_state=SEED, n_jobs=1
        ),
    }
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)
    results = {}
    for name, model in models.items():
        cv_auc = cross_val_score(model, x_train, y_train, cv=cv, scoring="roc_auc")
        model.fit(x_train, y_train)
        probabilities = model.predict_proba(x_test)[:, 1]
        predictions = model.predict(x_test)
        results[name] = {
            "cv_roc_auc_mean": float(cv_auc.mean()),
            "cv_roc_auc_std": float(cv_auc.std()),
            "test_roc_auc": float(roc_auc_score(y_test, probabilities)),
            "test_balanced_accuracy": float(balanced_accuracy_score(y_test, predictions)),
        }
    return results


if __name__ == "__main__":
    for name, metrics in run_experiment().items():
        print(name)
        for metric, value in metrics.items():
            print(f"  {metric}: {value:.4f}")
