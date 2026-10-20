# STAGE 02 — Multi-Cancer RNA-Seq Classification

**Status: complete, executed and verified.**

Public UCI gene-expression cancer RNA-Seq dataset: **801 samples, 20,531 features, five cancer types** (BRCA, COAD, KIRC, LUAD, PRAD).

## Direct access
- [Experiment source code](../stage2-rnaseq/rnaseq_analysis.py)
- [Dataset download and methodology](../stage2-rnaseq/README.md)
- [Verified JSON results](../stage2-rnaseq/results/rnaseq_metrics.json)
- [Scientific results summary](../stage2-rnaseq/results/research_summary.md)
- [Confusion matrix image](../stage2-rnaseq/figures/confusion_matrix.png)
- [Stage 3 robustness results](../stage2-rnaseq/results/stage3_research_report.md)
- [Automated test](../stage2-rnaseq/test_rnaseq.py)

## Verified Stage 2 results
| Metric | Result |
|---|---:|
| Five-fold CV accuracy | 99.84% |
| Held-out test accuracy | 99.38% (160/161) |
| Held-out test macro F1 | 99.47% |
| Selected expression features | 500 |

## Stage 3 robustness follow-up
- Repeated-CV macro F1: 99.87%
- Mean pairwise selected-feature Jaccard: 88.67%
- Features selected in all 15 fits: 423 of 500

**Limitations:** These are within-dataset results, not independent clinical validation. Anonymous expression feature indices are not established biomarkers.

This folder provides an accessible entry point while preserving the existing working analysis code under `stage2-rnaseq/`.
