import unittest
import numpy as np
from sklearn.datasets import make_classification
from rnaseq_analysis import evaluate

class TestRNASeq(unittest.TestCase):
    def test_synthetic_input(self):
        X, y = make_classification(n_samples=150, n_features=40, n_informative=12,
            n_classes=3, n_clusters_per_class=1, random_state=42)
        result = evaluate(X, np.array([f"class_{i}" for i in y]), n_features=15)
        self.assertEqual(result["dataset_shape"], [150, 40])
        self.assertEqual(result["selected_features"], 15)
        self.assertTrue(0 <= result["test_macro_f1"] <= 1)

if __name__ == "__main__":
    unittest.main()
