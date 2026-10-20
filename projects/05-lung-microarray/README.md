# Project 05 — Lung Microarray Cross-Cohort Study

**Separate research track from the UCI RNA-Seq study.** GPL96 microarray data: GSE10072 training, GSE7670 exploratory external comparison, GSE31547 locked third cohort.

## Source and reproducibility
- [Stage 5 baseline](src/cross_cohort_microarray.py)
- [Stage 6 domain shift](src/stage6_domain_shift.py)
- [Stage 7 locked test](src/stage7_third_cohort.py)
- [Stage 8 patient audit](src/stage8_patient_audit.py)
- [Processed GEO source-matrix reproduction](src/reproduce_source_matrices.py)
- [Locked Stage 7 protocol](protocols/STAGE7_LOCKED_PROTOCOL.md)

## Results
- [Stage 5 external metrics](results/cross_cohort_microarray.json)
- [Stage 6 normalization metrics](results/stage6_domain_shift.json)
- [Stage 7 locked metrics](results/stage7_third_cohort.json)
- [Stage 8 patient grouping](results/stage8_patient_independence_audit.json)
- [Reproduction and checksums](results/source_reproduction_audit.json)

## Manuscript
- [Consolidated manuscript](manuscript/lung_microarray_domain_shift_draft.md)
- [Scientific audit](manuscript/SCIENTIFIC_AUDIT.md)
- [Provenance addendum](manuscript/PROVENANCE_REPRODUCTION_ADDENDUM.md)

**Migration status:** Files are copied from the original tested paths; existing GitHub workflows remain canonical. No clinical utility or validated biomarkers are claimed.
