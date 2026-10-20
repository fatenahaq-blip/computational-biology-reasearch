# Scientific integrity and provenance audit — 20 October 2026

**Disposition: CONDITIONAL / NOT YET SUBMISSION-READY.** This audit verifies the repository's numerical outputs against saved experiment files and checks methods and public GEO records. It does not constitute independent replication from raw CEL files, original clinical chart review, or peer review.

## Audited evidence
- GEO [GSE10072](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE10072): 107 released profiles (58 tumor, 49 non-tumor). GEO states 180 initially selected, 148 passed RNA QC, 135 normalized, 13 excluded for low tumor cellularity, and 15 replicate measurements averaged into 107 final values. RMA-processed GPL96 array data.
- GEO [GSE7670](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE7670): 66 total profiles, including matched tissue samples, mixtures, commercial normal tissue and cell lines. The repository's title filters retain 52 tissue samples from 26 inferred patients; excluded categories should be rechecked against each GSM characteristic before journal submission.
- GEO [GSE31547](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE31547): 50 profiles (30 adenocarcinoma, 20 adjacent normal), GPL96, subseries of GSE31908. Sample [GSM782994](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM782994) explicitly reports quantile normalization and RMA using RMAExpress, with log2-transformed RMA values.
- Saved Stage 5, 6, 7 and 8 JSON results and committed source scripts were cross-checked for internal consistency.

## Verified internal arithmetic
- Stage 5 GSE7670 raw: confusion matrix [[26,0],[19,7]] -> 33/52 accuracy and 0.634615 balanced accuracy; tumor sensitivity 7/26.
- Stage 6 exploratory GSE7670 percentile ranks: [[26,0],[3,23]] -> 49/52 accuracy, 0.942308 balanced accuracy.
- Stage 7 GSE31547 locked percentile ranks: [[19,1],[0,30]] -> 49/50 accuracy, 0.975 balanced accuracy, sensitivity 30/30, specificity 19/20.
- Stage 8: 50 specimens but 43 unique numeric IDs extracted from sample titles. Seven IDs occur twice (8, 21, 22, 27, 44, 48, 83), each with a tumor and a normal sample. Cluster bootstrap balanced-accuracy percentile interval 0.9199–1.0000, conditional on inferred groups.

## Code audit
**Pass (limited code review):**
- ANOVA feature selection and standardization are inside the sklearn training pipeline.
- External outcome labels are not passed into model.fit, feature selection or the representation transform.
- Stage 7 uses fixed logistic-regression settings and threshold 0.5.
- Stage 7 protocol was committed before Stage 7 output generation, per repository history.
- GPL96 features are matched by probe identifiers, not positional columns.

**Critical qualifications:**
1. Stage 6 inspected GSE7670 outcomes before Stage 7 was designed. Percentile ranks were motivated by that exploration, so GSE7670 cannot be represented as untouched validation.
2. Stage 6 training-only selection rule **chose raw**, because all three representations tied on grouped CV balanced accuracy. Percentile rank is an exploratory hypothesis chosen for the subsequent locked test, not the winner of the pre-specified Stage 6 selection rule.
3. Stage 7 used a third GEO series, but no individual-level patient linkage across studies is available. Distinct GEO series and institutions support study-level separation, **not proof of patient-level non-overlap**.
4. GSE31547 contains repeated specimens by title-inferred patient IDs. The cluster bootstrap improves uncertainty accounting but depends on those identifiers being biologically valid.
5. A per-sample percentile transform uses the common probe intersection, which depends on feature availability in the external dataset but **not its outcome labels**. This is not outcome-label leakage, though it should be disclosed as target-feature-set alignment.
6. No raw CEL-file reprocessing, batch-effect decomposition, or independent replication by another analyst was conducted.
7. GSE10072's original study averaged technical replicates; do not describe 107 released profiles as 107 verified independent patients.
8. The prior Stage 7 Wilson intervals are specimen-level and should not be used as patient-independent intervals.
9. GSE7670 preprocessing is described in the repository as MAS5, but a full per-GSM processing audit has **not** been completed here; keep the claim provisional until verified directly from study sample records.
10. External ROC-AUC near 1 in a small selected case-control dataset does not imply reliable clinical diagnosis or screening.
11. The study is **microarray**, not RNA-Seq. The separate UCI five-cancer RNA-Seq project is not part of these external results.
12. The author must verify authorship contributions, institutional affiliation, ethics/data reuse terms, funding, and conflict-of-interest statements before submission.

## Citation audit
- Edgar R, Domrachev M, Lash AE. GEO: NCBI gene expression and hybridization array data repository. Nucleic Acids Res. 2002;30:207–210. DOI:10.1093/nar/30.1.207.
- Barrett T et al. NCBI GEO: archive for functional genomics data sets—update. Nucleic Acids Res. 2013;41:D991–D995. DOI:10.1093/nar/gks1193.
- Leek JT et al. Tackling the widespread and critical impact of batch effects in high-throughput data. Nat Rev Genet. 2010;11:733–739. DOI:10.1038/nrg2825.
- Bolstad BM et al. A comparison of normalization methods for high density oligonucleotide array data based on variance and bias. Bioinformatics. 2003;19:185–193. DOI:10.1093/bioinformatics/19.2.185.
- Primary dataset accessions: GSE10072, GSE7670, GSE31547. GSE10072 GEO lists PMID 18297132; GSE7670 lists PMIDs 17540040 and 19337377. The original paper titles/authors should be checked against PubMed before adding full citations.

## Outstanding requirements before journal/preprint submission
- Verify biological patient IDs using original sample characteristics or study documentation, including potential cross-study overlaps.
- Review all GSE7670 and GSE31547 sample metadata for inclusion criteria, paired specimens, histology and processing.
- Verify exact MAS5/RMA provenance and whether normalization was performed separately by cohort.
- Independently reproduce all outputs from source GEO series matrices, with package versions, source file checksums and frozen dependency lock.
- Review probe selection/annotation and check for batch, smoking, tumor stage and site confounding.
- Perform full primary-publication bibliography audit, author contribution and ethics statement checks.
- Decide whether to include inferential uncertainty or restrict to descriptive results if patient identities remain uncertain.

**Decision:** Suitable as a transparently qualified computational research portfolio and working manuscript; **not cleared as publication-ready scientific validation**.
