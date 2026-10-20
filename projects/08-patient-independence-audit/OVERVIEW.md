# Stage 08 — Patient Independence and Reproducibility

[Patient audit script](../05-lung-microarray/src/stage8_patient_audit.py) · [Audit tests](../05-lung-microarray/tests/test_stage8.py) · [Patient audit results](../05-lung-microarray/results/stage8_patient_independence_audit.json)

[Source-matrix reproduction script](../05-lung-microarray/src/reproduce_source_matrices.py) · [Verified checksums and reproduction metrics](../05-lung-microarray/results/source_reproduction_audit.json)

Seven title-inferred patient IDs appear twice; public processed GEO matrices were successfully re-executed. Cross-study patient identities and raw CEL reprocessing remain unverified.

The executable source remains with the shared lung microarray code until workflow migration is tested.
