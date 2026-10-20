# Computational Biology Research Portfolio

**Faten Tawfiq Abdelhaq** · Independent Researcher

Reproducible educational and exploratory computational biology research. **Eight stages, organized as eight numbered project folders.** The lung microarray study is separate from the multi-cancer RNA-Seq study.

## Research stages

| Stage | Research project | Evidence |
|---|---|---|
| **01** | [Breast Cancer Feature Classification](projects/01-breast-cancer-classification/OVERVIEW.md) | [Validated results](projects/01-breast-cancer-classification/results/validated-results.md) |
| **02** | [Multi-Cancer RNA-Seq Classification](projects/02-multicancer-rnaseq/OVERVIEW.md) | [Verified metrics](projects/02-multicancer-rnaseq/results/rnaseq_metrics.json) |
| **03** | [RNA-Seq Statistical Robustness](projects/03-rnaseq-robustness/OVERVIEW.md) | [Stability metrics](projects/03-rnaseq-robustness/results/stage3_stability.json) |
| **04** | [External Validation Readiness](projects/04-validation-readiness/OVERVIEW.md) | [Readiness audit](projects/04-validation-readiness/results/stage4_readiness.json) |
| **05** | [Independent Lung Microarray Cohort](projects/05-lung-microarray/OVERVIEW.md) | [External results](projects/05-lung-microarray/results/cross_cohort_microarray.json) |
| **06** | [Domain Shift and Normalization](projects/06-domain-shift/OVERVIEW.md) | [Comparison metrics](projects/05-lung-microarray/results/stage6_domain_shift.json) |
| **07** | [Locked Third-Cohort Validation](projects/07-locked-third-cohort/OVERVIEW.md) | [Third-cohort results](projects/05-lung-microarray/results/stage7_third_cohort.json) |
| **08** | [Patient Independence and Reproducibility Audit](projects/08-patient-independence-audit/OVERVIEW.md) | [Audit results](projects/05-lung-microarray/results/stage8_patient_independence_audit.json) |

## Results and scientific manuscript

- **[Results dashboard — all eight stages](RESEARCH_RESULTS.md)**
- [Consolidated lung microarray manuscript](manuscript/lung_microarray_domain_shift_draft.md)
- [Scientific integrity audit](manuscript/SCIENTIFIC_AUDIT.md)
- [Provenance, citations and reproduction](manuscript/PROVENANCE_REPRODUCTION_ADDENDUM.md)

## Reproducibility and repository status

The `projects/` folders present the organized research materials. The original `src/`, `stage2-rnaseq/`, `tests/` and `.github/workflows/` paths are temporarily retained to preserve the already-tested execution workflows. These legacy paths will be retired only after the new layout passes independent workflow checks.

**Scientific scope:** Stage 01 uses image-derived nucleus measurements; Stages 02–04 use RNA-Seq; Stages 05–08 analyze a distinct GPL96 microarray study. This portfolio is not a peer-reviewed publication or clinically validated diagnostic system.
