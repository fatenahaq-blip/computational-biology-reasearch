# RNA-Seq experiment: reproducible results

Dataset: UCI gene expression cancer RNA-Seq, 801 samples, five classes.
Methods: training-only feature selection within five-fold stratified CV,
standardization and logistic regression.

- Training CV accuracy: 0.9984 (SD 0.0031)
- Training CV macro F1: 0.9987
- Held-out test accuracy: 0.9938
- Held-out test macro F1: 0.9947

![Held-out confusion matrix](../figures/confusion_matrix.png)

## Interpretation and limitations
This is a single-dataset tissue classification demonstration, not a clinical
diagnostic model. Strong scores may reflect large differences between tissue
types. Batch effects, cohort confounding, model selection uncertainty and
absence of external validation limit generalizability. Selected feature
indices are not verified biological gene symbols or validated biomarkers.
