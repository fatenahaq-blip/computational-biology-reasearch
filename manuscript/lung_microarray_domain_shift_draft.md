# Cross-Cohort Generalization of Lung Cancer Gene-Expression Classifiers: An Exploratory Evaluation of Domain Shift and Within-Sample Rank Normalization

**Faten Tawfiq Abdelhaq**  
Independent Researcher

**Manuscript status:** Working scientific manuscript, not peer reviewed or submitted. Patient-level provenance audit pending. Results concern **microarray** gene-expression measurements, not RNA sequencing. This work is separate from the earlier five-cancer UCI RNA-Seq demonstration.

## Abstract

**Background:** High within-study classification accuracy may not generalize to independent gene-expression cohorts because of differences in preprocessing, sample composition and technical effects. We evaluated a lung tumor-versus-normal microarray classifier across studies and investigated whether a label-free within-sample rank representation could improve transportability.

**Methods:** A logistic-regression pipeline with training-only ANOVA selection of 200 shared Affymetrix GPL96 probes was trained on GSE10072 (107 specimens). Grouped cross-validation estimated internal performance. The locked raw-expression model was evaluated on GSE7670 (52 selected patient-tissue specimens). Three representations—raw expression, fixed log2 transformation and per-sample percentile ranks—were then compared in an exploratory analysis; model selection used training-only cross-validation. A percentile-rank model, specified and committed before outcome evaluation, was subsequently assessed on the previously unused GSE31547 cohort (50 specimens). No external labels were used to fit the models.

**Results:** Raw-expression grouped training cross-validation yielded 97.78% balanced accuracy, but external balanced accuracy on GSE7670 was 63.46% (tumor sensitivity 7/26). In the post-hoc comparison, percentile ranks yielded 94.23% balanced accuracy on GSE7670 (23/26 tumors identified), versus 50.00% with the log2 representation. All three representations tied on the training-only balanced-accuracy criterion; therefore the pre-specified selection rule still favored raw expression. In the separately locked GSE31547 evaluation, percentile ranks achieved 97.50% balanced accuracy, ROC-AUC 0.965, and 49/50 correctly classified specimens. GSE31547 included only 43 unique patient identifiers inferred from titles across 50 specimens; patient-level independence remains under audit.

**Conclusions:** Cross-cohort performance differed markedly from internal validation. Sample-wise percentile ranks showed promising exploratory transportability and strong performance in a third study under a locked protocol. Findings remain limited by cohort heterogeneity, preprocessing differences, specimen dependence, small sample sizes and lack of clinical validation.

**Keywords:** lung adenocarcinoma; microarray; domain shift; cross-cohort validation; machine learning; percentile ranks; reproducibility.

## 1. Introduction

Biomedical machine-learning models frequently perform well under within-dataset cross-validation but degrade when evaluated on independent cohorts. Differences in acquisition platforms, preprocessing, patient populations, tissue handling and outcome definitions can cause distribution shift. Gene-expression studies are particularly sensitive to normalization choices, because absolute measurement scales may differ even when probes are nominally comparable.

The present study investigated the transportability of a binary lung tumor-versus-normal classifier across public Affymetrix GPL96 microarray datasets. We first documented the external performance gap of a raw-expression model. We then explored two label-free expression transformations and performed a separately locked evaluation of a percentile-rank pipeline in a third study. The goal was methodological evaluation, not development of a clinical diagnostic assay or discovery of new biomarkers.

## 2. Materials and methods

### 2.1 Data sources and cohort roles

Public gene-expression series were obtained from the NCBI Gene Expression Omnibus (GEO). GSE10072 supplied 107 training specimens (58 tumor and 49 normal) and 74 title-inferred patient groups. GSE7670 supplied 52 selected patient-tissue specimens (26 tumor and 26 normal) from 26 title-inferred patient groups. Mixed tissue preparations, cell lines and other excluded sample types were not used for this evaluation. GSE31547 supplied 50 specimens (30 tumor and 20 normal), with 43 distinct identifiers inferred from specimen titles. The third cohort was not used during the earlier normalization exploration.

All three studies used Affymetrix GPL96 microarrays. The comparison aligned 22,215 shared probe identifiers after excluding AFFX control probes. Feature correspondence was established by probe identifier, not matrix position. This is a microarray analysis and should not be conflated with the separate UCI RNA-Seq five-cancer experiment.

### 2.2 Initial classification and internal validation

The raw-expression pipeline used training-only univariate ANOVA F-statistic selection of 200 probes, standardization, and logistic regression (maximum 3,000 iterations; random seed 42). GroupKFold with five splits was used for internal evaluation, keeping specimens assigned to the same title-inferred patient group together. Feature selection and scaling were refitted within each training fold. The full GSE10072 training set was then used to fit the model for external testing on GSE7670.

### 2.3 Exploratory normalization sensitivity analysis

We compared (i) raw published expression values, (ii) fixed log2(max(x, 0) + 1), and (iii) within-sample percentile ranks computed across aligned probes. Each representation was applied separately to samples and required no outcome labels or external-cohort-fitted parameters. Each representation was embedded in the same training-only feature-selection and classification pipeline.

The selection criterion was training grouped-CV balanced accuracy; ties favored the raw representation. External performance was reported for **all** three methods. GSE7670 results had already been observed during initial experimentation, so this analysis was explicitly exploratory and post hoc, even though external labels were not used for fitting or method selection.

### 2.4 Locked third-cohort evaluation

A Stage 7 protocol was committed to the GitHub repository before evaluating GSE31547 outcomes. It fixed the percentile-rank representation, shared probe alignment, 200-feature ANOVA selection on GSE10072 only, standardization on GSE10072 only, logistic regression, and a classification threshold of 0.5. The resulting model was applied once to GSE31547 without outcome-dependent modification. The primary endpoint was balanced accuracy; secondary endpoints included sensitivity, specificity, macro F1 and ROC-AUC.

### 2.5 Independence and uncertainty

The initial third-cohort result included specimen-level Wilson intervals for sensitivity and specificity. However, 50 specimens corresponded to 43 title-inferred identifiers, indicating possible within-patient dependence. A separate patient-level audit and group-resampling analysis was initiated; until its results and original sample provenance are reviewed, specimen-level intervals are descriptive rather than definitive patient-independent inference.

### 2.6 Reproducibility

All code, protocol files, unit tests and machine-readable metrics are maintained in the public repository [Computational Biology Research](https://github.com/fatenahaq-blip/computational-biology-reasearch). GitHub Actions execute the experiments and save results. The repository contains no redistributed raw patient expression matrix.

## 3. Results

### 3.1 Internal versus external performance

Grouped internal cross-validation of the raw-expression pipeline on GSE10072 achieved mean balanced accuracy 0.9778 and mean ROC-AUC 1.0000. On GSE7670, the locked raw model achieved balanced accuracy 0.6346, F1 0.4242 and ROC-AUC 0.6538. It correctly identified all 26 normal specimens but only 7 of 26 tumor specimens.

### 3.2 Exploratory normalization comparison

| Representation | Training CV balanced accuracy | GSE7670 balanced accuracy | GSE7670 ROC-AUC | Tumor sensitivity | Normal specificity |
|---|---:|---:|---:|---:|---:|
| Raw | 0.9778 | 0.6346 | 0.6538 | 0.2692 | 1.0000 |
| Log2 | 0.9778 | 0.5000 | 0.9985 | 0.0000 | 1.0000 |
| Percentile rank | 0.9778 | 0.9423 | 1.0000 | 0.8846 | 1.0000 |

Although percentile ranks performed best externally in this exploratory comparison, the training-only selection rule chose raw expression because the internal balanced-accuracy scores were tied. The log2 model's high ROC-AUC alongside zero tumor sensitivity at threshold 0.5 illustrates the distinction between ranking discrimination and calibrated threshold transfer.

### 3.3 Locked third-cohort evaluation

The percentile-rank pipeline achieved balanced accuracy 0.9750, macro F1 0.9790 and ROC-AUC 0.9650 on GSE31547. It classified 30/30 tumor specimens and 19/20 normal specimens correctly, corresponding to 49/50 correct classifications. The confusion matrix (normal/tumor rows and columns) was [[19, 1], [0, 30]]. Descriptive specimen-level Wilson 95% intervals were 0.8865–1.0000 for sensitivity and 0.7639–0.9911 for specificity.

### 3.4 Patient-level audit

**Pending final audit results.** The automated title-based check identified 43 distinct title-inferred patient identifiers among 50 specimens. The number and nature of repeated identifiers, mixed tumor/normal specimen groups, and patient-cluster bootstrap uncertainty will be inserted after the Stage 8 workflow completes. No claim of 50 independent patients is made.

## 4. Discussion

The pronounced reduction from internal balanced accuracy (97.78%) to raw-expression external balanced accuracy (63.46%) highlights the risk of relying on within-study validation. In the exploratory sensitivity analysis, within-sample percentile ranks were associated with substantially better cross-cohort performance. Rank transformations may attenuate global scale differences without estimating target-cohort normalization parameters, although they can also discard potentially informative absolute expression variation.

The locked third-cohort result supports the plausibility of the rank-based approach beyond the dataset used to generate the hypothesis. Nevertheless, high performance on a single additional cohort cannot demonstrate broad clinical generalizability. Study-specific biology, preprocessing, tissue selection, sampling and repeated specimens remain possible sources of bias.

The nearly perfect log2 ROC-AUC with zero sensitivity at the default decision threshold in GSE7670 also indicates that score ordering and threshold transportability should be evaluated separately. Future work should include calibration assessed without target-label tuning and patient-group-aware uncertainty estimates.

### 4.1 Limitations

This is an observational computational study using curated public microarray datasets, not RNA-Seq, prospective screening or a clinically validated assay. GSE10072 and GSE7670 differ in published preprocessing (RMA versus MAS5); this may contribute to domain shift but has not been isolated causally. The small external cohorts, title-inferred patient identifiers, possible specimen dependence and post-hoc development of the rank-based hypothesis limit inferential strength. The GPL96 probe identifiers have not been used to establish novel or clinically validated biomarkers. Results may be sensitive to the study-specific inclusion rules and to the choice of preprocessing.

### 4.2 Next steps

Complete the patient-level metadata audit; report cluster-aware uncertainty; document original cohort provenance and preprocessing in a supplementary evidence table; examine additional genuinely unused studies; and assess verified probe-to-gene mapping and pathway analysis only with appropriately controlled annotation and multiple-testing procedures.

## 5. Conclusion

Cross-study evaluation exposed substantial deterioration in raw-expression lung tissue classification performance despite strong internal validation. A label-free percentile-rank representation produced promising exploratory results and retained high performance under a locked evaluation on a third microarray cohort. The evidence supports further investigation of rank-based cross-cohort robustness, not claims of clinical diagnostic validity or novel biomarker discovery.

## Data availability and code

Original data are available from GEO under accessions [GSE10072](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE10072), [GSE7670](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE7670) and [GSE31547](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE31547). Code, locked protocol and results are available at the GitHub repository linked above.

## Ethics statement

This computational study uses publicly available, previously collected and de-identified gene-expression data. Institutional review and dataset-specific reuse requirements should be checked before journal submission.

## Funding and conflicts of interest

Funding: No external funding reported for this independent portfolio study.  
Conflicts of interest: To be confirmed by the author before submission.

## References (bibliographic audit pending)

1. Edgar R, Domrachev M, Lash AE. Gene Expression Omnibus: NCBI gene expression and hybridization array data repository. *Nucleic Acids Research*. 2002;30(1):207–210. https://doi.org/10.1093/nar/30.1.207
2. Barrett T, et al. NCBI GEO: archive for functional genomics data sets—update. *Nucleic Acids Research*. 2013;41(D1):D991–D995. https://doi.org/10.1093/nar/gks1193
3. Leek JT, et al. Tackling the widespread and critical impact of batch effects in high-throughput data. *Nature Reviews Genetics*. 2010;11:733–739. https://doi.org/10.1038/nrg2825
4. Bolstad BM, Irizarry RA, Åstrand M, Speed TP. A comparison of normalization methods for high density oligonucleotide array data based on variance and bias. *Bioinformatics*. 2003;19(2):185–193. https://doi.org/10.1093/bioinformatics/19.2.185
5. GSE10072, GSE7670 and GSE31547: original GEO series records, linked in Data availability. Original study articles and dataset-specific sample annotations require final citation audit.
