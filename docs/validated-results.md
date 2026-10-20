# Validated experiment results

Executed 20 October 2026 using scikit-learn 1.8.0.

| Metric | Logistic regression | Random forest |
|---|---:|---:|
| Mean five-fold training CV ROC-AUC | 0.9959 | 0.9894 |
| CV ROC-AUC standard deviation | 0.0050 | 0.0086 |
| Held-out test ROC-AUC | 0.9954 | 0.9931 |
| Held-out test balanced accuracy | 0.9812 | 0.9504 |

Commands: `python -m src.train` and `python -m unittest discover -s tests`. Automated test passed (1 test).

These results use the Wisconsin Diagnostic Breast Cancer dataset of **image-derived cell nucleus measurements, not gene-expression data**. They are educational and do not demonstrate clinical validity or original biological discoveries. External validation, calibration and bias assessment remain outstanding.
