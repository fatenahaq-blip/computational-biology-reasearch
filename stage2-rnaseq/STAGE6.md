# Stage 6 — Domain shift and label-free normalization

**Status:** Experimental code and workflow published; real-data results pending successful run.

## Question
Can pre-specified, label-free expression transformations improve external classification of lung tumor vs normal tissue between GSE10072 and GSE7670?

## Compared methods
1. Raw published expression (Stage 5 baseline).
2. Fixed sample-wise log2(max(x,0)+1) transformation.
3. Sample-wise percentile ranks of shared GPL96 probes.

All methods are applied separately to each sample and do not use external outcome labels or fit cohort-wide normalization statistics.

## Leakage safeguards
- Only GSE10072 is used for grouped 5-fold cross-validation and selection of the preferred representation.
- The representation, top-200 ANOVA feature selection, standardization and logistic regression are contained in one training pipeline.
- The chosen method maximizes training grouped-CV balanced accuracy; ties favor the raw baseline.
- All three external-cohort scores are reported, including failures. No external scores influence method selection.

## Important qualification
Stage 5 already exposed the GSE7670 labels and results. This is therefore a **post-hoc exploratory sensitivity analysis**, even though the Stage 6 code does not use external labels for training or method selection. A new untouched cohort is necessary for confirmatory external validation.

## Execution
```bash
python -m pip install -r requirements.txt
python -m unittest -v test_stage6.py
python stage6_domain_shift.py
```
The workflow publishes `results/stage6_domain_shift.json`.

## Interpretation
Differences in RMA versus MAS5 preprocessing, sample composition, probe distributions and cohort selection may contribute to domain shift. A change in accuracy does not alone establish which mechanism caused it. Percentile ranks can discard meaningful absolute expression information. Neither normalization nor classification accuracy validates a biomarker or clinical tool.
