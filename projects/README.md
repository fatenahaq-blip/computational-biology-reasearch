# Research Projects

| Project | Focus | Verified evidence |
|---|---|---|
| [01 — Breast Cancer Classification](01-breast-cancer-classification/) | Image-derived cell measurements, educational ML | [Results](01-breast-cancer-classification/results/validated-results.md) |
| [02 — Multi-Cancer RNA-Seq](02-multicancer-rnaseq/) | Five cancer classes | [Metrics](02-multicancer-rnaseq/results/rnaseq_metrics.json) |
| [03 — RNA-Seq Robustness](03-rnaseq-robustness/) | Feature stability, repeated CV | [Metrics](03-rnaseq-robustness/results/stage3_stability.json) |
| [04 — Validation Readiness](04-validation-readiness/) | Feature identity and cohort audit safeguards | [Readiness](04-validation-readiness/results/stage4_readiness.json) |
| [05 — Lung Microarray](05-lung-microarray/) | Cross-cohort generalization, normalization, locked test, patient audit | [Stage 7](05-lung-microarray/results/stage7_third_cohort.json) |

**Migration note:** This is an additive, reviewable layout. Canonical scripts in `src/` and `stage2-rnaseq/` remain untouched until imports and workflows are fully migrated and retested. Do not delete the legacy directories yet.
