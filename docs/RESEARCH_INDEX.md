# Research Portfolio — Project and Stage Index

**Faten Tawfiq Abdelhaq · Independent Researcher**

This page is the navigation hub for the portfolio. The first two stages are present in the repository; they were not deleted. Stages 3–8 extend the two research tracks.

| Stage | Project | Source | Results / report |
|---|---|---|---|
| **1** | Breast cancer image-derived feature classification (educational demonstration) | [src/train.py](../src/train.py) | [Validated results](../docs/validated-results.md) |
| **2** | Five-cancer RNA-Seq classification, UCI dataset 401 | [stage2-rnaseq/rnaseq_analysis.py](../stage2-rnaseq/rnaseq_analysis.py) | [Metrics](../stage2-rnaseq/results/rnaseq_metrics.json) · [Summary](../stage2-rnaseq/results/research_summary.md) |
| **3** | RNA-Seq robustness and feature-selection stability | [stage3_stability.py](../stage2-rnaseq/stage3_stability.py) | [Metrics](../stage2-rnaseq/results/stage3_stability.json) · [Report](../stage2-rnaseq/results/stage3_research_report.md) |
| **4** | External-cohort readiness and feature-mapping safeguards | [stage4_external_audit.py](../stage2-rnaseq/stage4_external_audit.py) | [Readiness](../stage2-rnaseq/results/stage4_readiness.json) |
| **5** | Lung microarray independent-cohort evaluation | [cross_cohort_microarray.py](../stage2-rnaseq/cross_cohort_microarray.py) | [Report](../stage2-rnaseq/results/stage5_external_cohort_report.md) |
| **6** | Domain shift and label-free normalization | [stage6_domain_shift.py](../stage2-rnaseq/stage6_domain_shift.py) | [Report](../stage2-rnaseq/results/stage6_domain_shift_report.md) |
| **7** | Locked third-cohort microarray evaluation | [stage7_third_cohort.py](../stage2-rnaseq/stage7_third_cohort.py) | [Protocol](../stage2-rnaseq/STAGE7_LOCKED_PROTOCOL.md) · [Report](../stage2-rnaseq/results/stage7_third_cohort_report.md) |
| **8** | Patient clustering and provenance audit | [stage8_patient_audit.py](../stage2-rnaseq/stage8_patient_audit.py) | [Audit results](../stage2-rnaseq/results/stage8_patient_independence_audit.json) |

## Consolidated manuscript and research integrity

- [Consolidated lung microarray manuscript](../manuscript/lung_microarray_domain_shift_draft.md)
- [Scientific audit](../manuscript/SCIENTIFIC_AUDIT.md)
- [Provenance and reproduction addendum](../manuscript/PROVENANCE_REPRODUCTION_ADDENDUM.md)
- [Source-matrix reproduction evidence](../stage2-rnaseq/results/source_reproduction_audit.json)

## Important distinctions

**Stage 1:** The Wisconsin breast cancer dataset uses image-derived cell-nucleus measurements, not gene expression.

**Stages 2–4:** UCI five-cancer RNA-Seq classification and its within-dataset robustness work. Stage 4 is a compatibility framework, not an independent validation result.

**Stages 5–8:** A separate lung tumor-versus-normal **microarray** research track using GEO datasets GSE10072, GSE7670 and GSE31547. Do not combine its scores with the UCI RNA-Seq experiment as though they are the same study.

The research is exploratory and is not a peer-reviewed publication, validated clinical tool or novel biomarker claim.
