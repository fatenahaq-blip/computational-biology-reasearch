# Stage 3 — Statistical robustness and feature-selection stability

**Status:** Executed successfully using the UCI gene expression cancer RNA-Seq dataset (801 samples, 20,531 anonymous expression features; five tissue labels). This is an exploratory computational biology portfolio study, not a clinical validation or peer-reviewed publication.

## Research question
Does five-class tumor tissue classification remain accurate across resampled training folds, and how consistent are the selected expression features?

## Methods
A fixed stratified 80/20 split yielded 640 training and 161 held-out test samples. The training data were evaluated with 5-fold stratified cross-validation repeated three times (15 folds). In each fit, ANOVA selected 500 features within the training fold, followed by standardization and class-balanced logistic regression. A majority-class classifier provided a baseline. Pairwise Jaccard overlap assessed feature-set similarity across folds. A 2,000-resample percentile bootstrap on the fixed test predictions summarized conditional uncertainty in test accuracy.

## Results
| Metric | Value |
|---|---:|
| Mean repeated-CV macro F1 | 0.998657 |
| SD across CV folds | 0.002685 |
| Majority-class baseline macro F1 | 0.109091 |
| Mean pairwise selected-feature Jaccard | 0.886658 |
| Features selected in all 15 fits | 423 / 500 |
| Held-out test accuracy | 0.993789 (160 / 161) |
| Held-out test macro F1 | 0.994711 |
| Test accuracy bootstrap percentile interval (95%) | 0.981366–1.000000 |

## Interpretation
The model performs very strongly on this curated five-tissue dataset and substantially exceeds the majority-class baseline. Feature-selection overlap is high across resampled training folds, with 423 of 500 anonymous features selected in all 15 fits.

## Limitations
- **Not external validation.** Both cross-validation and held-out testing use the same source dataset.
- The labels distinguish cancer tissue types rather than cancer versus healthy tissue. Results cannot be interpreted as cancer detection performance.
- Cross-validation folds overlap; the fold SD is descriptive and is not an inferential confidence interval.
- The bootstrap interval is conditional on a single trained model and held-out sample. It does not quantify transportability or external generalization.
- The 20,531 feature indices are anonymous and cannot be responsibly named as specific genes without verified feature mapping.
- Potential batch effects, tissue-of-origin confounding, cohort selection bias and prospective clinical performance remain unassessed.
- Analyses were developed iteratively after Stage 2 results were observed, so results are exploratory.

## Reproducibility
Source: `stage2-rnaseq/stage3_stability.py`
Machine-readable results: `stage2-rnaseq/results/stage3_stability.json`
Automated workflow: `.github/workflows/stage3-rnaseq.yml`

## Future work
Independent external cohort evaluation, feature annotation using verified gene IDs, pathway enrichment with multiple-testing control, and sensitivity analysis of model and preprocessing choices.
