# Stage 5 — Independent-cohort microarray evaluation

**Status:** Experiment executed successfully; exploratory research result. This is a **new lung tumor-versus-normal microarray study**, not an external test of the Stage 2 five-cancer RNA-Seq model.

## Design
- Training study: GSE10072, 107 samples (49 normal, 58 tumor), 74 patient groups.
- Independent study: GSE7670, 52 patient-tissue samples (26 normal, 26 tumor), 26 patient groups.
- Shared platform: GPL96; 22,215 common probe IDs.
- Training-only top-200 ANOVA feature selection, scaling, logistic regression; grouped 5-fold cross-validation.
- Locked model applied to GSE7670 without external-cohort fitting.

## Verified results

| Metric | Result |
|---|---:|
| Training grouped-CV balanced accuracy | 0.977778 |
| Training grouped-CV ROC-AUC | 1.000000 |
| External accuracy | 0.634615 |
| External balanced accuracy | 0.634615 |
| External F1 | 0.424242 |
| External ROC-AUC | 0.653846 |

External confusion matrix (actual rows: normal, tumor; predicted columns: normal, tumor):

| | Predicted normal | Predicted tumor |
|---|---:|---:|
| Actual normal | 26 | 0 |
| Actual tumor | 19 | 7 |

External tumor sensitivity: **7/26 = 26.9%**. Normal specificity: **26/26 = 100%**.

## Interpretation
The gap between within-study cross-validation and independent-cohort evaluation shows poor transportability of the fitted classifier under the current processing and cohort conditions. This negative result is valuable research evidence and should be reported transparently rather than hidden.

## Limitations
- GSE10072 uses RMA-normalized expression while GSE7670 uses MAS5-scaled values; differences in normalization may cause domain shift, but causation has not been demonstrated.
- Study populations, patient characteristics, and tumor subtypes may differ.
- No external normalization was fitted using test labels; no adaptation experiment has yet been performed.
- The study is microarray-based, not RNA-Seq.
- These data cannot establish clinical diagnostic performance, gene causality or validated biomarkers.
- The original UCI RNA-Seq feature mapping remains unresolved.

## Next preregistered-style sensitivity analyses
1. Inspect per-study probe distributions and quality control without consulting external outcome labels.
2. Compare log-scale and rank-based representations using training-only model selection, clearly documenting any post hoc exploratory choices.
3. Re-evaluate on untouched independent data if an additional cohort is available.
4. Map probes to verified GPL96 annotations before any pathway analysis.
5. Report uncertainty intervals for external sensitivity and specificity.

Source metrics: [cross_cohort_microarray.json](cross_cohort_microarray.json).
