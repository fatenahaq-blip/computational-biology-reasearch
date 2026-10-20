# Stage 05 — Independent Lung Microarray Cohort

**Research track:** Lung microarray cross-cohort generalization.

- [Analysis code](src/cross_cohort_microarray.py)
- [Patient filtering test](tests/test_cross_cohort.py)
- [Verified metrics](results/cross_cohort_microarray.json)
- [Scientific report](results/stage5_external_cohort_report.md)

Training: GSE10072. External: GSE7670. Raw-expression external balanced accuracy: 63.46%.

**Limitation:** This is a GPL96 microarray study, not the Stage 2 RNA-Seq model.
