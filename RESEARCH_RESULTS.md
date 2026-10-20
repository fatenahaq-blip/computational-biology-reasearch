# RESEARCH RESULTS — Overview

**Faten Tawfiq Abdelhaq | Independent Researcher**

This page presents the verified results in human-readable form. All figures refer to specific datasets and experiments; **do not compare metrics across different tasks as if they measured the same clinical problem.**

## Stage 1 — Breast Cancer Image-Derived Feature Classification
**[Open Stage 1](projects/01-breast-cancer-classification/OVERVIEW.md)**

| Result | Logistic regression | Random forest |
|---|---:|---:|
| Test ROC-AUC | 99.54% | 99.31% |
| Test balanced accuracy | 98.12% | 95.04% |

[Validation evidence](docs/validated-results.md)

## Stage 2 — Five-Cancer RNA-Seq Classification
**[Open Stage 2](projects/02-multicancer-rnaseq/OVERVIEW.md)**

| Metric | Result |
|---|---:|
| Samples / features | 801 / 20,531 |
| Test accuracy | **99.38%** (160/161) |
| Test macro F1 | 99.47% |
| Five-fold CV accuracy | 99.84% |

[Full results](stage2-rnaseq/results/rnaseq_metrics.json) · [Confusion matrix](stage2-rnaseq/figures/confusion_matrix.png)

## Stage 3 — RNA-Seq Statistical Robustness
| Metric | Result |
|---|---:|
| Repeated-CV macro F1 | 99.87% |
| Mean selected-feature Jaccard | 88.67% |
| Features consistently selected | 423 / 500 |

[Stage 3 report](stage2-rnaseq/results/stage3_research_report.md)

## Stage 4 — External Validation Readiness
A compatibility and annotation audit framework was built. **No external RNA-Seq validation was completed for the Stage 2 model.**

[Stage 4 methodology](stage2-rnaseq/STAGE4.md)

## Stage 5 — Independent Lung Microarray Cohort
**Different study and task from Stage 2 RNA-Seq.** Training: GSE10072; external cohort: GSE7670.

| Metric | Result |
|---|---:|
| Training grouped-CV balanced accuracy | 97.78% |
| External raw-expression balanced accuracy | **63.46%** |
| External tumor sensitivity | 7/26 (26.92%) |

[Stage 5 report](stage2-rnaseq/results/stage5_external_cohort_report.md)

## Stage 6 — Domain Shift and Normalization
Exploratory external performance on GSE7670:

| Representation | Balanced accuracy | Tumor sensitivity |
|---|---:|---:|
| Raw expression | 63.46% | 26.92% |
| Log2 | 50.00% | 0% |
| Percentile ranks | **94.23%** | 88.46% |

**Caution:** Training CV selected raw expression by its pre-specified tie-breaker. Percentile ranks were investigated as a post-hoc hypothesis.

[Stage 6 report](stage2-rnaseq/results/stage6_domain_shift_report.md)

## Stage 7 — Locked Third-Cohort Test
Training: GSE10072; third cohort: GSE31547 (50 specimens).

| Metric | Result |
|---|---:|
| Balanced accuracy | **97.50%** |
| ROC-AUC | 0.965 |
| Tumor sensitivity | 30/30 |
| Normal specificity | 19/20 |

[Locked protocol](stage2-rnaseq/STAGE7_LOCKED_PROTOCOL.md) · [Stage 7 report](stage2-rnaseq/results/stage7_third_cohort_report.md)

## Stage 8 — Patient Grouping and Reproducibility Audit
- 50 specimens corresponded to **43 title-inferred patient groups**.
- Seven groups contained paired tumor and normal specimens.
- Patient-cluster bootstrap balanced-accuracy 95% percentile interval: **91.99%–100%**, conditional on title-derived grouping.
- Public processed GEO matrices were successfully re-downloaded and the published computational results reproduced.

[Patient audit](stage2-rnaseq/results/stage8_patient_independence_audit.json) · [Reproduction evidence](stage2-rnaseq/results/source_reproduction_audit.json)

## Consolidated scientific manuscript
[Read manuscript draft](manuscript/lung_microarray_domain_shift_draft.md) · [Scientific audit](manuscript/SCIENTIFIC_AUDIT.md)

**Research integrity:** These are exploratory research and educational outputs, not peer-reviewed clinical evidence, a validated diagnostic tool or verified novel biomarkers.
