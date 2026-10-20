import unittest
import pandas as pd
from stage4_external_audit import audit

class TestStage4Audit(unittest.TestCase):
    def test_missing_mapping_blocks(self):
        result = audit(["feature_1", "feature_2"], ["ENSG1", "ENSG2"],
                       ["train1"], ["external1", "external2"],
                       ["BRCA", "KIRC"])
        self.assertEqual(result["status"], "blocked")
        self.assertIn("No verified source-feature-to-gene mapping supplied", result["issues"])

    def test_verified_one_to_one_mapping(self):
        mapping = pd.DataFrame({"source_feature": ["feature_1", "feature_2"],
                                "gene_id": ["ENSG1", "ENSG2"]})
        result = audit(["feature_1", "feature_2"], ["ENSG1", "ENSG2"],
                       ["train1"], ["external1", "external2"],
                       ["BRCA", "KIRC"], mapping)
        self.assertEqual(result["status"], "compatible_for_further_review")

    def test_overlapping_sample_blocks(self):
        mapping = pd.DataFrame({"source_feature": ["f1"], "gene_id": ["g1"]})
        result = audit(["f1"], ["g1"], ["same"], ["same", "other"],
                       ["BRCA", "KIRC"], mapping)
        self.assertEqual(result["status"], "blocked")

if __name__ == "__main__":
    unittest.main()
