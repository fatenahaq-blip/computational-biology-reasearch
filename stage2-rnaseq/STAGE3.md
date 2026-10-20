# Stage 3 — RNA-Seq robustness and feature stability

**Status: analysis code and workflow prepared; real-data Stage 3 results pending successful execution.**

This extension evaluates the robustness of the Stage 2 five-class cancer tissue classification model on UCI dataset 401.

## Methods
- Preserve the same fixed stratified 80/20 train/test split (seed 42).
- Perform **5-fold repeated stratified cross-validation with 3 repeats** on training data only.
- Fit ANOVA top-500 feature selection and standardization *inside each fold* before logistic regression.
- Compare macro F1 with a most-frequent-class dummy baseline.
- Measure feature-selection stability using mean pairwise Jaccard similarity and count features selected in all 15 fits.
- Bootstrap the **fixed held-out test predictions** 2,000 times to describe sampling uncertainty in test accuracy.

## Run
```bash
python -m pip install -r requirements.txt
python -m unittest -v test_stage3.py
python stage3_stability.py
```

Outputs: `results/stage3_stability.json`.

## Important scientific limitations
- Repeated cross-validation folds overlap; fold scores are not independent, and the reported standard deviation is **not** a confidence interval.
- The bootstrap percentile interval conditions on the trained model and observed test cohort; it does not measure performance on a genuinely external cohort.
- Feature indices are anonymous, not validated gene identifiers. A stable index is **not** a biomarker.
- Stage 3 uses the same underlying dataset as Stage 2. It is not external validation and should not be described as such.
- Selection of analysis choices after inspecting Stage 2 performance introduces exploratory analysis bias.
- No claims of clinical diagnosis, biological causality, or novel biomarker discovery.
