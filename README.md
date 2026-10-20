# Computational Biology Research — Start Here

**Faten Tawfiq Abdelhaq · Independent Researcher**

## Research projects and results

| Project | Status | Open |
|---|---|---|
| **STAGE 01 — Breast Cancer Classification** | Completed educational experiment | **[Open Stage 1](STAGE-01-Breast-Cancer-Classification/README.md)** |
| **STAGE 02 — Multi-Cancer RNA-Seq** | Executed and verified | **[Open Stage 2](STAGE-02-Multi-Cancer-RNA-Seq/README.md)** |
| **STAGES 03–08 — Advanced Research** | Experiments, audits and reports | [View all stages](docs/RESEARCH_INDEX.md) |

### **[VIEW ALL VERIFIED RESULTS — HUMAN-READABLE DASHBOARD](RESEARCH_RESULTS.md)**

### [Read consolidated research manuscript](manuscript/lung_microarray_domain_shift_draft.md)

The first two folders are now visible at the top level. Existing code remains in `src/` and `stage2-rnaseq/` so working experiment paths are preserved.

---

# Computational Biology Research Portfolio

**Faten Tawfiq Abdelhaq · Independent Researcher**

## Start here — All research stages

**[Open the complete Stage 1–8 Research Index](docs/RESEARCH_INDEX.md)**

### First two research projects

**Stage 1 — Breast Cancer Feature Classification:** [Python experiment](src/train.py) · [Validated results](docs/validated-results.md)

**Stage 2 — Multi-Cancer RNA-Seq Classification:** [Project overview](stage2-rnaseq/README.md) · [Python experiment](stage2-rnaseq/rnaseq_analysis.py) · [Verified metrics](stage2-rnaseq/results/rnaseq_metrics.json)

### Advanced research and manuscript

**Stages 3–8:** [Robustness, external cohorts, normalization and patient audit](docs/RESEARCH_INDEX.md)

**Consolidated lung microarray manuscript:** [Read draft](manuscript/lung_microarray_domain_shift_draft.md)

**Scientific integrity:** [Audit](manuscript/SCIENTIFIC_AUDIT.md) · [Reproduction evidence](stage2-rnaseq/results/source_reproduction_audit.json)

> Research distinction: Stage 1 uses image-derived cell-nucleus features; Stages 2–4 use RNA-Seq; Stages 5–8 are a separate microarray research track. All work is exploratory and not clinically validated.

---

# Computational Biology Research Portfolio

**Faten Abdelhaq** | Medical graduate · Python and machine learning learner · Aspiring computational biology researcher

This repository documents reproducible educational experiments in biomedical data analysis and statistical learning. It is a developing portfolio, **not a record of peer-reviewed publications or clinically validated tools**.

## Experiment 1 — Breast cancer diagnostic feature classification

This experiment uses the public Wisconsin Diagnostic Breast Cancer dataset bundled with scikit-learn. The features are derived from images of cell nuclei; **this is not gene-expression data**. Logistic regression and random forest are compared using stratified five-fold cross-validation on the training partition and evaluation on a held-out test partition.

### Run locally

```bash
python -m pip install -r requirements.txt
python -m src.train
python -m unittest discover -s tests
```

The script prints cross-validation ROC AUC (mean and standard deviation), test ROC AUC and balanced accuracy. Results have been executed and checked; see [validated results](docs/validated-results.md). No identifiable patient data is included.

## Research interests

- Biomedical machine learning and robust model validation
- Computational genomics and gene-expression analysis (planned)
- Interpretability, reproducibility and dataset shift
- Clinical relevance, bias and responsible AI

## Next research direction

A gene-expression classification study using an openly licensed dataset, with transparent preprocessing, leakage controls, sample-level splitting and limitations. **Planned; not yet completed.**

## Limitations

This educational demonstration does not establish clinical utility. The dataset is small and curated; external cohort validation, calibration, fairness evaluation and prospective assessment would be necessary for clinical use.

See [research roadmap](docs/research-roadmap.md).
