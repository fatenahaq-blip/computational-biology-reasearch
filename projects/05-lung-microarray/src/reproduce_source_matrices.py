"""Independent source-matrix reproduction with SHA256 provenance and strict metric comparison."""
import hashlib, json, platform, sys
from pathlib import Path
import numpy as np, pandas as pd, sklearn, scipy
from cross_cohort_microarray import prepare, parse_geo_matrix, URLS
from stage6_domain_shift import experiment
from stage7_third_cohort import load_third_cohort, evaluate_locked
from stage8_patient_audit import audit
BASE=Path(__file__).resolve().parent
def sha256_url(url):
    import urllib.request
    h=hashlib.sha256()
    with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"research-reproducibility/1.0"}),timeout=180) as response:
        while True:
            chunk=response.read(1048576)
            if not chunk: break
            h.update(chunk)
    return h.hexdigest()
def close(actual,expected,label,tol=1e-10):
    if not np.isclose(actual,expected,rtol=0,atol=tol):
        raise AssertionError(f"{label}: expected {expected}, obtained {actual}")
def main():
    train,y,groups=prepare("GSE10072")
    ext,ye,ge=prepare("GSE7670")
    shared=train.columns.intersection(ext.columns,sort=False)
    shared=shared[~shared.str.startswith("AFFX-",na=False)]
    stage6=experiment(train.loc[:,shared],y,groups,ext.loc[:,shared],ye)
    expected6=json.loads((BASE/"results/stage6_domain_shift.json").read_text())
    for method in ("raw","log2","percentile_rank"):
        for metric in ("balanced_accuracy","roc_auc","tumor_sensitivity","normal_specificity"):
            close(stage6["external_results_all_methods"][method][metric],
                  expected6["external_results_all_methods"][method][metric],
                  f"Stage 6 {method} {metric}")
    third,yt,ids=load_third_cohort()
    stage7=evaluate_locked(train,y,third,yt,ids)
    expected7=json.loads((BASE/"results/stage7_third_cohort.json").read_text())
    for metric in ("balanced_accuracy","roc_auc","tumor_sensitivity","normal_specificity"):
        close(stage7[metric],expected7[metric],f"Stage 7 {metric}")
    stage8=audit()
    expected8=json.loads((BASE/"results/stage8_patient_independence_audit.json").read_text())
    if stage8["repeated_id_counts"]!=expected8["repeated_id_counts"]:
        raise AssertionError("Stage 8 inferred patient grouping changed")
    if stage8["external_confusion_matrix"]!=expected8["external_confusion_matrix"]:
        raise AssertionError("Stage 8 confusion matrix changed")
    URLS["GSE31547"]="https://ftp.ncbi.nlm.nih.gov/geo/series/GSE31nnn/GSE31547/matrix/GSE31547_series_matrix.txt.gz"
    hashes={name:sha256_url(URLS[name]) for name in ("GSE10072","GSE7670","GSE31547")}
    result={"status":"independently_reexecuted_from_public_processed_GEO_series_matrices",
            "raw_CEL_reprocessing":False,"training_samples":len(y),"external_samples":len(ye),
            "third_samples":len(yt),"stage6_external_balanced_accuracy":{m:v["balanced_accuracy"] for m,v in stage6["external_results_all_methods"].items()},
            "stage7_balanced_accuracy":stage7["balanced_accuracy"],
            "stage8_inferred_patient_groups":stage8["n_unique_title_patient_ids"],
            "source_series_matrix_sha256":hashes,
            "software":{"python":sys.version.split()[0],"numpy":np.__version__,"pandas":pd.__version__,"scikit_learn":sklearn.__version__,"scipy":scipy.__version__,"platform":platform.platform()},
            "limitations":["Same codebase and data processing, separate automated rerun; not an independent analyst replication.",
                           "Uses GEO processed matrices, not original raw CEL reprocessing.",
                           "Patient identities across studies remain unverified."]}
    out=BASE/"results/source_reproduction_audit.json"
    out.write_text(json.dumps(result,indent=2),encoding="utf-8")
    print(json.dumps(result,indent=2))
if __name__=="__main__":main()
