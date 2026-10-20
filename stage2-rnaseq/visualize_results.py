"""Generate reproducible figures and a summary from actual RNA-Seq metrics."""
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

BASE = Path(__file__).resolve().parent
source = BASE / "results" / "rnaseq_metrics.json"
if not source.exists():
    raise SystemExit("No validated results found. Run rnaseq_analysis.py first.")
data = json.loads(source.read_text(encoding="utf-8"))
classes = data["classes"]
cm = np.asarray(data["confusion_matrix"], dtype=int)
if cm.shape != (len(classes), len(classes)):
    raise ValueError("Confusion matrix shape does not match class labels.")
out = BASE / "figures"
out.mkdir(exist_ok=True)
fig, ax = plt.subplots(figsize=(7, 6))
im = ax.imshow(cm, cmap="Blues")
ax.set_xticks(range(len(classes)), classes, rotation=45, ha="right")
ax.set_yticks(range(len(classes)), classes)
ax.set_xlabel("Predicted cancer type")
ax.set_ylabel("True cancer type")
ax.set_title("Held-out test confusion matrix")
for (i, j), value in np.ndenumerate(cm):
    ax.text(j, i, str(value), ha="center", va="center",
            color="white" if value > cm.max() / 2 else "black")
fig.colorbar(im, ax=ax)
fig.tight_layout()
fig.savefig(out / "confusion_matrix.png", dpi=180)
plt.close(fig)
report = f"""# RNA-Seq experiment: reproducible results

Dataset: UCI gene expression cancer RNA-Seq, 801 samples, five classes.
Methods: training-only feature selection within five-fold stratified CV,
standardization and logistic regression.

- Training CV accuracy: {data['cv_accuracy_mean']:.4f} (SD {data['cv_accuracy_std']:.4f})
- Training CV macro F1: {data['cv_macro_f1_mean']:.4f}
- Held-out test accuracy: {data['test_accuracy']:.4f}
- Held-out test macro F1: {data['test_macro_f1']:.4f}

![Held-out confusion matrix](../figures/confusion_matrix.png)

## Interpretation and limitations
This is a single-dataset tissue classification demonstration, not a clinical
diagnostic model. Strong scores may reflect large differences between tissue
types. Batch effects, cohort confounding, model selection uncertainty and
absence of external validation limit generalizability. Selected feature
indices are not verified biological gene symbols or validated biomarkers.
"""
(BASE / "results" / "research_summary.md").write_text(report, encoding="utf-8")
print("Saved figures/confusion_matrix.png and results/research_summary.md")
