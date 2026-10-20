# Stage 06 — Domain Shift and Normalization

**Track:** Lung microarray cross-cohort generalization.

[Python analysis](../05-lung-microarray/src/stage6_domain_shift.py) · [Tests](../05-lung-microarray/tests/test_stage6.py) · [Verified metrics](../05-lung-microarray/results/stage6_domain_shift.json) · [Scientific report](../05-lung-microarray/results/stage6_domain_shift_report.md)

Exploratory GSE7670 external balanced accuracy: raw 63.46%, log2 50.00%, percentile ranks 94.23%.

The Stage 6 training-only selection rule favored raw expression after a tie. Percentile ranks were investigated post hoc and require independently locked evaluation. This is microarray, not RNA-Seq.

The executable source remains with the shared lung microarray code until workflow migration is tested.
