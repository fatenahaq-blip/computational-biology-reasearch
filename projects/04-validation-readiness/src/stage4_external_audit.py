"""Stage 4: external-cohort compatibility audit; no unsupported biological claims."""
import argparse
import json
from pathlib import Path
import numpy as np
import pandas as pd

EXPECTED_CLASSES = {"BRCA", "COAD", "KIRC", "LUAD", "PRAD"}

def audit(train_features, external_features, train_sample_ids, external_sample_ids,
          external_labels, gene_mapping=None):
    """Audit data compatibility before external validation.

    Feature names must be verified biological identifiers or a documented,
    one-to-one mapping. No automatic positional feature alignment is permitted.
    """
    a, b = list(map(str, train_features)), list(map(str, external_features))
    train_ids, ext_ids = set(map(str, train_sample_ids)), set(map(str, external_sample_ids))
    labels = set(map(str, external_labels))
    issues = []
    if len(a) != len(set(a)) or len(b) != len(set(b)):
        issues.append("Duplicate feature identifiers")
    if len(ext_ids) != len(list(external_sample_ids)):
        issues.append("Duplicate external sample identifiers")
    if train_ids & ext_ids:
        issues.append("Overlapping training and external sample IDs")
    if not labels.issubset(EXPECTED_CLASSES):
        issues.append("External labels outside the five training classes")
    if len(labels) < 2:
        issues.append("External cohort has fewer than two represented classes")
    if gene_mapping is None:
        issues.append("No verified source-feature-to-gene mapping supplied")
        mapped = []
    else:
        if not {"source_feature", "gene_id"}.issubset(gene_mapping.columns):
            issues.append("Mapping must contain source_feature and gene_id")
            mapped = []
        else:
            mapping = gene_mapping.dropna(subset=["source_feature", "gene_id"]).copy()
            mapping["source_feature"] = mapping["source_feature"].astype(str)
            mapping["gene_id"] = mapping["gene_id"].astype(str)
            if mapping["source_feature"].duplicated().any() or mapping["gene_id"].duplicated().any():
                issues.append("Mapping is not one-to-one")
            mapping_dict = dict(zip(mapping["source_feature"], mapping["gene_id"]))
            mapped = [mapping_dict[x] for x in a if x in mapping_dict]
            if len(mapped) != len(a):
                issues.append("Incomplete training feature annotation")
            if set(mapped) != set(b):
                issues.append("External gene identifiers do not exactly match mapped training features")
    return {
        "status": "blocked" if issues else "compatible_for_further_review",
        "issues": issues,
        "n_training_features": len(a),
        "n_external_features": len(b),
        "n_external_samples": len(list(external_sample_ids)),
        "n_mapped_features": len(mapped),
        "represented_classes": sorted(labels),
        "note": "Compatibility does not establish biological comparability, batch equivalence, or external model validity."
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--training-features", required=True, help="CSV with feature_id column")
    p.add_argument("--training-samples", required=True, help="CSV with sample_id column")
    p.add_argument("--external-expression", required=True, help="CSV: sample_id plus gene ID columns")
    p.add_argument("--external-labels", required=True, help="CSV: sample_id,label")
    p.add_argument("--mapping", help="Verified CSV: source_feature,gene_id")
    p.add_argument("--output", default="results/stage4_audit.json")
    args = p.parse_args()
    train_feat = pd.read_csv(args.training_features)["feature_id"].astype(str).tolist()
    train_ids = pd.read_csv(args.training_samples)["sample_id"].astype(str).tolist()
    external = pd.read_csv(args.external_expression)
    labels = pd.read_csv(args.external_labels)
    if "sample_id" not in external or not {"sample_id", "label"}.issubset(labels):
        raise ValueError("Missing required sample_id or label columns")
    if external["sample_id"].duplicated().any() or labels["sample_id"].duplicated().any():
        raise ValueError("Duplicate external sample IDs")
    labels = labels.set_index("sample_id").reindex(external["sample_id"])
    if labels["label"].isna().any():
        raise ValueError("External expression and label samples do not match")
    values = external.drop(columns=["sample_id"]).apply(pd.to_numeric, errors="raise").to_numpy()
    if not np.isfinite(values).all():
        raise ValueError("Non-finite external expression values")
    mapping = pd.read_csv(args.mapping) if args.mapping else None
    result = audit(train_feat, external.columns.drop("sample_id"), train_ids,
                   external["sample_id"].astype(str).tolist(),
                   labels["label"].astype(str).tolist(), mapping)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    if result["status"] == "blocked":
        raise SystemExit(2)

if __name__ == "__main__":
    main()
