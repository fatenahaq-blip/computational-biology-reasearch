# Stage 7 — Locked third-cohort evaluation

**Status: completed with verified results.** The protocol was committed before the Stage 7 outcome evaluation in `STAGE7_LOCKED_PROTOCOL.md`.

## Question
Does the exploratory percentile-rank representation identified in Stage 6 retain strong performance on a previously unused lung-cancer tissue cohort under fixed training and evaluation rules?

## Design
- Training: GSE10072 (107 samples).
- Third-cohort evaluation: GSE31547 (50 specimens; 30 tumors, 20 adjacent normal tissues).
- Platform: GPL96 Affymetrix **microarray**, not RNA-Seq.
- Shared GPL96 probes: 22,215; training-only ANOVA selection of 200.
- Sample-wise percentile ranks, training-fitted standardization, logistic regression, threshold 0.5.
- No model fitting, feature selection, normalization fitting or threshold optimization using GSE31547 outcomes.

## Verified results

| Endpoint | Result |
|---|---:|
| Balanced accuracy | 0.9750 |
| Macro F1 | 0.978983 |
| ROC-AUC | 0.9650 |
| Tumor sensitivity | 30/30 = 1.000 |
| Normal specificity | 19/20 = 0.950 |
| Correct classifications | 49/50 |

Confusion matrix (actual normal/tumor rows; predicted normal/tumor columns): `[[19,1],[0,30]]`.

Descriptive Wilson 95% specimen-level intervals:
- Tumor sensitivity: 0.8865–1.0000.
- Normal specificity: 0.7639–0.9911.

## Interpretation
The locked percentile-rank pipeline performed strongly on a third, previously unused study, supporting the hypothesis that a within-sample rank representation may improve cross-cohort transportability compared with untransformed expression. This result is consistent with, but does not prove, a normalization-driven explanation for Stage 5 domain shift.

## Essential caveats
1. The third cohort contains 50 specimens but only 43 distinct patient identifiers inferred from titles. Some specimens may be related; patient-level independence and provenance must be verified before interpreting confidence intervals inferentially.
2. This study is microarray-based; it does not externally validate the separate five-class RNA-Seq model.
3. The percentile-rank approach was motivated by exploratory findings on GSE7670. Stage 7 was locked before the third-cohort evaluation, but it is not a prospective clinical trial.
4. This small, curated case-control study does not establish screening, clinical diagnostic validity or generalization across all institutions and platforms.
5. Feature IDs are microarray probes; no novel biomarkers or causal genes have been established.

## Reproducibility
- Protocol: [STAGE7_LOCKED_PROTOCOL.md](../STAGE7_LOCKED_PROTOCOL.md)
- Script: [stage7_third_cohort.py](../stage7_third_cohort.py)
- Machine-readable metrics: [stage7_third_cohort.json](stage7_third_cohort.json)

## Next checks
Audit the third-cohort sample-to-patient mapping, confirm independence of tissue samples, and compare performance under patient-level resampling. Avoid post-hoc tuning against this cohort.
