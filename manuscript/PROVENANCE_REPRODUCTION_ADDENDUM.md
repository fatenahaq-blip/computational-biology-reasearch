# Final provenance, citations, and independent reproduction addendum — 20 October 2026

## Biological identity assessment
- **GSE10072:** original study describes 107 released expression profiles after averaging 15 technical replicate measurements; the GEO sample titles contain 74 distinct GT-number identifiers. These are title-derived identifiers, not proof of 74 unique clinical persons. The Landi et al. study describes paired non-tumor and adenocarcinoma tissue from the EAGLE study.
- **GSE7670:** GEO explicitly describes **27 paired tumor–normal patient pairs**, with additional mixtures, commercial tissue and cell lines. The model's stricter title filter retained **26 paired patients (52 specimens)**; the excluded 27th pair must be reconciled with the original GEO metadata before making a claim that all eligible surgical samples were included.
- **GSE31547:** GEO lists **30 tumors and 20 adjacent normal tissues**. Seven repeated numerical specimen-title IDs were found in both tumor and normal records; the code inferred 43 distinct title IDs. The original records do not independently certify these numbers as unique biological patient identifiers.
- **Cross-study non-overlap:** the studies originate from different research submissions/institutions, but there is no harmonized patient identifier or linkage registry. **No definitive individual-level non-overlap can be claimed.**

## Preprocessing provenance
- GSE10072 GEO GSM processed values: **RMA signal**; the original Landi et al. paper documents technical replicate averaging and quality filtering.
- GSE7670 original Su et al. BMC Genomics paper describes **MAS5.0 intensity processing** and separately discusses RMA comparisons. The exact GEO series-matrix processing lineage and whether it represents MAS5 or a subsequently processed expression matrix should still be checked against representative GSM records and matrix metadata; do not overstate universal per-sample processing confirmation.
- GSE31547 representative GEO GSM records state **quantile normalization and RMA via RMAExpress**; processed values are log2-transformed RMA signal.
- The classifier consumes GEO **processed series matrices**. Reprocessing raw CEL files under one harmonized pipeline would constitute a distinct sensitivity study, not reproduction of the published matrix-based result.

## Verified primary citations
1. Landi MT, Dracheva T, Rotunno M, et al. Gene expression signature of cigarette smoking and its role in lung adenocarcinoma development and survival. *PLoS ONE*. 2008;3(2):e1651. DOI: [10.1371/journal.pone.0001651](https://doi.org/10.1371/journal.pone.0001651). PMID:18297132. Dataset GSE10072.
2. Su LJ, Chang CW, Wu YC, et al. Selection of DDX5 as a novel internal control for Q-RT-PCR from microarray data using a block bootstrap re-sampling scheme. *BMC Genomics*. 2007;8:140. DOI: [10.1186/1471-2164-8-140](https://doi.org/10.1186/1471-2164-8-140). PMID:17540040. Dataset GSE7670.
3. GSE31547: Girard L, Minna JD, Gerald WL, Saintigny P, Zhang L (GEO contributors). *MSKCC-A Primary Lung Cancer Specimens*. NCBI GEO series GSE31547, released 2011. The GEO record does **not** provide a primary publication citation. Do not invent one. https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE31547
4. Edgar R, Domrachev M, Lash AE. Gene Expression Omnibus: NCBI gene expression and hybridization array data repository. *Nucleic Acids Res*. 2002;30(1):207–210. DOI:10.1093/nar/30.1.207.
5. Barrett T, et al. NCBI GEO: archive for functional genomics data sets—update. *Nucleic Acids Res*. 2013;41(D1):D991–D995. DOI:10.1093/nar/gks1193.
6. Leek JT, et al. Tackling the widespread and critical impact of batch effects in high-throughput data. *Nat Rev Genet*. 2010;11:733–739. DOI:10.1038/nrg2825.
7. Bolstad BM, Irizarry RA, Åstrand M, Speed TP. A comparison of normalization methods for high density oligonucleotide array data based on variance and bias. *Bioinformatics*. 2003;19(2):185–193. DOI:10.1093/bioinformatics/19.2.185.

## Reproduction protocol
`stage2-rnaseq/reproduce_source_matrices.py` independently re-downloads the three GEO **processed series matrices**, re-executes the Stage 6 and Stage 7 model pipelines, reproduces Stage 8 grouping checks, compares results with published JSON values and records SHA256 checksums plus package versions. The workflow `.github/workflows/reproduce-source-matrices.yml` executes it.

**Execution status:** The script and workflow have been committed. Successful execution and matching metrics are **not yet confirmed** until `stage2-rnaseq/results/source_reproduction_audit.json` appears and is inspected. This is a rerun by the same codebase, not independent analyst replication or raw CEL reprocessing.

## Submission decision
**Conditional / not fully publication-cleared.** Public-record patient grouping and literature provenance are substantially better documented. Original biological identity across cohorts, source-matrix preprocessing lineage at individual GSM level, and independent raw-CEL replication remain unresolved. Do not claim these have been conclusively established.
