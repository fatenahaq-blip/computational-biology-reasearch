# Stage 7 — Locked third-cohort protocol

**Registered in repository before the Stage 7 outcome evaluation.**

## Hypothesis
A percentile-rank representation of microarray expression will yield better cross-study transportability than the raw expression approach observed in exploratory Stage 5–6 experiments.

## Dataset roles
- **Training only:** GSE10072 (GPL96; 107 samples).
- **Previously explored:** GSE7670 (GPL96). Its outcomes informed the hypothesis but will not enter Stage 7 model fitting or evaluation.
- **Held-out confirmation:** GSE31547 (GPL96; 30 tumor and 20 normal tissue samples according to GEO metadata). No Stage 7 outcomes have been inspected for this study at the time of protocol registration.

## Locked choices
1. Use only shared GPL96 probe identifiers across training and third cohort; drop `AFFX-` control probes. Align by probe identifier, never by column position.
2. Include only GSE31547 sample titles exactly matching `numberL(A)` (tumor) or `numberNL(A)` (normal). Assert 30 tumors and 20 normals; fail closed if metadata differ.
3. Training samples and labels use the unchanged GSE10072 parser.
4. Transform **each sample separately** into average-tie percentile ranks of its shared probes. No pooled cohort fitting, external-label transformations, or outcome-dependent normalization.
5. Select 200 probes with ANOVA F test on GSE10072 only; standardize on GSE10072 only; train logistic regression with `max_iter=3000`, `random_state=42`, default threshold 0.5.
6. Evaluate once on all 50 GSE31547 samples, without fitting, tuning, threshold optimization or feature selection on the third cohort.
7. Primary endpoint: balanced accuracy. Secondary endpoints: tumor sensitivity, normal specificity, macro F1, ROC-AUC, confusion matrix.
8. Calculate 95% Wilson intervals for tumor sensitivity and specificity (descriptive, not adjusted for any within-patient correlation).
9. Do not modify the model in response to Stage 7 scores. If the workflow fails for technical reasons, document and correct the technical problem without using third-cohort outcomes for tuning.

## Scientific caveats
- GSE31547 may contain multiple specimens from a patient; assess sample independence using metadata before formal claims of inferential uncertainty.
- Both classes are distinct tissue types; results do not demonstrate screening or clinical diagnostic validity.
- The exploratory development of the percentile-rank hypothesis used GSE7670; the third-cohort test is therefore a new validation of an existing, previously explored hypothesis, not evidence of a fully prospective clinical trial.
- Probe-level model features are not validated gene biomarkers.
- A successful test on a single new study cannot establish broad transportability.
