# Stage 2: Multi-Cancer RNA-Seq Classification

**Status: full dataset analysis executed and verified; see [recorded metrics](results/rnaseq_metrics.json), [scientific summary](results/research_summary.md), and [Stage 3 robustness](results/stage3_research_report.md).** This is an educational computational biology portfolio project, not a peer-reviewed publication or clinical tool.

## Research question
Can expression features distinguish five cancer tissue types in a curated public RNA-Seq dataset?

## Dataset and attribution
Fiorini, S. (2016). *gene expression cancer RNA-Seq*. UCI Machine Learning Repository. DOI: [10.24432/C5R88H](https://doi.org/10.24432/C5R88H). License: CC BY 4.0. UCI dataset ID 401. 801 samples and 20,531 expression features; labels BRCA, COAD, KIRC, LUAD, PRAD. The repository does **not** redistribute raw data.

## Methods
- Stratified 80/20 train/test split (random seed 42).
- Five-fold stratified cross-validation on the training partition.
- ANOVA feature selection, standardization and class-balanced logistic regression **inside the pipeline**, avoiding training/validation leakage.
- Accuracy, macro F1, class-level metrics and confusion matrix on held-out test data.
- Selected feature indices are anonymous UCI feature identifiers, **not validated biomarkers**.

## Run
From the `stage2-rnaseq` directory:

```bash
python -m pip install -r requirements.txt
python rnaseq_analysis.py
python -m unittest -v test_rnaseq.py
```

The first command that runs the analysis downloads the UCI dataset and requires internet access. Output: `results/rnaseq_metrics.json`. The test uses synthetic data and does not require the dataset.

## Verification and limitations
The synthetic-data unit test passed locally. **The complete UCI dataset analysis has been executed and verified in GitHub Actions.** This dataset is small relative to its feature count; tissue-of-origin confounding, batch effects, class imbalance and lack of external validation limit biological and clinical interpretation. The feature IDs are anonymized, so pathway-level biological interpretation requires mapping back to verified gene identifiers. No diagnostic or biomarker claims are made.
