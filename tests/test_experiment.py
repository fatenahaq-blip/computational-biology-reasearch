import unittest
from src.train import run_experiment


class TestExperiment(unittest.TestCase):
    def test_metrics_in_range(self):
        results = run_experiment()
        self.assertEqual(set(results), {"logistic_regression", "random_forest"})
        for metrics in results.values():
            for value in metrics.values():
                self.assertGreaterEqual(value, 0)
                self.assertLessEqual(value, 1)


if __name__ == "__main__":
    unittest.main()
