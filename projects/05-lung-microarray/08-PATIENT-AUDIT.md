# Stage 08 — Patient Independence and Reproducibility Audit

- [Patient audit code](src/stage8_patient_audit.py)
- [Tests](tests/test_stage8.py)
- [Verified patient audit](results/stage8_patient_independence_audit.json)
- [Source-matrix reproduction code](src/reproduce_source_matrices.py)
- [Reproduction results and checksums](results/source_reproduction_audit.json)
- [Scientific integrity audit](manuscript/SCIENTIFIC_AUDIT.md)
- [Provenance addendum](manuscript/PROVENANCE_REPRODUCTION_ADDENDUM.md)

50 specimens correspond to 43 title-inferred identifiers; seven IDs have paired tumor and normal samples. Automated reproduction from public processed GEO matrices succeeded.

**Limitation:** Biological patient identity across studies and raw CEL-file reproduction are not independently verified.
