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

The script prints cross-validation ROC AUC (mean and standard deviation), test ROC AUC and balanced accuracy. No numerical performance is claimed here without execution and review. No identifiable patient data is included.

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
