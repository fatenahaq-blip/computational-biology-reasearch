# Stage 06 — Domain Shift and Label-Free Normalization

- [Analysis code](src/stage6_domain_shift.py)
- [Tests](tests/test_stage6.py)
- [Verified metrics](results/stage6_domain_shift.json)
- [Scientific report](results/stage6_domain_shift_report.md)

Exploratory external balanced accuracy on GSE7670: raw 63.46%, log2 50.00%, percentile ranks 94.23%.

**Important:** Training-only cross-validation tied across methods, and the specified tie-break rule selected raw. Percentile ranks were a post-hoc research hypothesis, not the prospectively selected winner.
