# Independent-cohort lung expression study (Stage 5)

**Experiment:** GSE10072 training -> GSE7670 independent external testing.

**Important:** This is a NEW binary tumor-versus-normal **microarray** study, not an external test of the five-class UCI RNA-Seq model. Do not compare its accuracy as though the tasks were identical.

## Data provenance
- [GSE10072](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE10072): 107 lung tumor/noninvolved tissue expression profiles, GPL96 Affymetrix array; RMA-normalized.
- [GSE7670](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE7670): GPL96 Affymetrix array, includes paired surgical tissues, mixed tissues, commercial tissue and cell lines. Only numbered patient adenocarcinoma tissue samples are eligible for external testing; other samples are excluded.

## Safeguards
- Shared GPL96 **probe IDs** are matched by identifier, not by column order.
- Patient IDs are grouped during training cross-validation to reduce leakage between matched tissue samples.
- Feature selection and scaling occur inside each training fold.
- The model is trained on GSE10072 and evaluated without refitting on GSE7670.
- External results are interpreted cautiously because RMA and MAS5 normalization differ substantially across cohorts.

## Run
```bash
python -m pip install -r requirements.txt
python -m unittest -v test_cross_cohort.py
python cross_cohort_microarray.py
```

Results are saved to `results/cross_cohort_microarray.json` if the analysis succeeds.

## Status
Code and workflow published; full independent-cohort run and metrics pending verification. **No external performance claims until the results file is inspected.**
