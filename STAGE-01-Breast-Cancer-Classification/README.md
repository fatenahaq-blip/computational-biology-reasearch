# STAGE 01 — Breast Cancer Feature Classification

**Status: completed educational experiment; results verified.**

This experiment uses the Wisconsin Diagnostic Breast Cancer dataset. Its input features are **measurements derived from images of cell nuclei, not gene expression or RNA sequencing**.

## Direct access
- [Python experiment](../src/train.py)
- [Automated tests](../tests/test_experiment.py)
- [Validated experimental results](../docs/validated-results.md)
- [Dependencies](../requirements.txt)

## Verified results
| Metric | Logistic regression | Random forest |
|---|---:|---:|
| Training 5-fold CV ROC-AUC | 0.9959 | 0.9894 |
| Held-out test ROC-AUC | 0.9954 | 0.9931 |
| Held-out test balanced accuracy | 98.12% | 95.04% |

**Limitations:** Small curated dataset; no external validation, clinical diagnostic claims or gene-level biomarker findings.

This folder is a dedicated project entry point. The existing working source files remain in their original locations to preserve reproducibility.
