import unittest
import numpy as np
from sklearn.datasets import make_classification
from stage3_stability import validate_stability

class TestStage3(unittest.TestCase):
    def test_synthetic_stability(self):
        X, y = make_classification(n_samples=120, n_features=30, n_informative=10,
                                    n_classes=3, n_clusters_per_class=1, random_state=42)
        r = validate_stability(X, np.array([f"class_{i}" for i in y]),
                               n_features=10, n_splits=3, n_repeats=2)
        self.assertEqual(r["n_features_selected_per_fit"], 10)
        self.assertEqual(r["cv_folds"], 3)
        self.assertTrue(0 <= r["mean_pairwise_feature_jaccard"] <= 1)
        self.assertEqual(len(r["test_accuracy_bootstrap_percentile_95"]), 2)

if __name__ == "__main__":
    unittest.main()
