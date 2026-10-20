# Stage 6 — Label-free normalization and cross-cohort domain shift

**Exploratory, post-hoc analysis.** GSE10072 training (107 samples) and GSE7670 external evaluation (52 patient-tissue samples). Same GPL96 microarray probe platform. This is **not** RNA-Seq and is not an external test of the original UCI five-cancer RNA-Seq classifier.

## Research question
Can sample-wise, label-free expression transformations reduce cross-cohort performance degradation without using external outcome labels in fitting, feature selection or training-only model selection?

## Methods
Three fixed representations were evaluated: raw expression, log2(max(x,0)+1), and within-sample percentile ranks. Each pipeline used training-only top-200 ANOVA feature selection, standardization and logistic regression. Grouped 5-fold training cross-validation selected the preferred method by balanced accuracy, with ties favoring raw. All three representations were then evaluated on the independent GSE7670 cohort. The external outcomes were not used for model fitting or selecting the preferred method, but had already been inspected during Stage 5.

## Verified results

| Metric | Raw | Log2 | Percentile rank |
|---|---:|---:|---:|
| Training CV balanced accuracy | 0.977778 | 0.977778 | 0.977778 |
| External balanced accuracy | 0.634615 | 0.500000 | 0.942308 |
| External F1 | 0.424242 | 0.000000 | 0.938776 |
| External ROC-AUC | 0.653846 | 0.998521 | 1.000000 |
| External tumor sensitivity | 0.269231 | 0.000000 | 0.884615 |
| External normal specificity | 1.000000 | 1.000000 | 1.000000 |

Confusion matrices (rows actual normal/tumor; columns predicted normal/tumor):
- Raw: [[26, 0], [19, 7]]
- Log2: [[26, 0], [26, 0]]
- Percentile rank: [[26, 0], [3, 23]]

Training-only method selection: **raw**, because all methods tied on grouped-CV balanced accuracy and the pre-specified tie rule favored raw.

## Label-free distribution diagnostics

| Representation | Training median | External median | Approx. pooled-value Wasserstein |
|---|---:|---:|---:|
| Raw | 7.4275 | 213.8 | 775.3779 |
| Log2 | 3.0751 | 7.7469 | 4.5582 |
| Percentile rank | 0.5000 | 0.5000 | 0.000969 |

These diagnostics describe marginal scale differences; percentile ranks enforce a common marginal distribution by construction and do **not** establish removal of biological batch effects.

## Interpretation
Within-sample percentile ranks achieved markedly higher external classification performance in this exploratory comparison. The result is consistent with sensitivity to differences in expression scale across studies, but it does not prove that normalization alone caused the change or that the approach will generalize. The log2 model's near-perfect ROC-AUC but zero tumor sensitivity at the default threshold demonstrates that threshold transfer and probability calibration matter.

## Limitations
1. GSE7670 labels and Stage 5 results were already examined before Stage 6; this is **not** a pristine, untouched external validation.
2. Percentile ranks were not selected by the specified training-only criterion; presenting them as the validated winning method would be misleading.
3. The two studies have different expression preprocessing (RMA versus MAS5), populations and potentially different biology; confounding remains.
4. 52 external samples from 26 patient groups are relatively few; paired observations are not independent.
5. External ROC-AUC of 1.0 in this small dataset does not establish clinical utility or prospective diagnostic performance.
6. No gene-level biomarker discovery, independent pathway interpretation or prospective validation was performed.

## Next study
Pre-specify percentile ranks and threshold calibration **using training data only**, then evaluate them in a third untouched cohort, with patient-level uncertainty intervals, metadata checks, and complete code/data provenance.

Source: [stage6_domain_shift.json](stage6_domain_shift.json).
