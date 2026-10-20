import unittest
import numpy as np
from stage6_domain_shift import SampleRepresentation

class TestStage6(unittest.TestCase):
    def test_rank_independent_of_other_samples(self):
        a = np.array([[4., 1., 2., 3.]])
        b = np.array([[100., 50., 20., 10.]])
        t = SampleRepresentation("percentile_rank")
        single = t.transform(a)[0]
        together = t.transform(np.vstack([a, b]))[0]
        np.testing.assert_allclose(single, together)
    def test_log_is_fixed_and_finite(self):
        x = np.array([[-2., 0., 3.]])
        np.testing.assert_allclose(SampleRepresentation("log2").transform(x),
                                   np.log2(np.array([[1., 1., 4.]])))
    def test_raw_no_change(self):
        x = np.array([[1., 3.]])
        np.testing.assert_array_equal(SampleRepresentation("raw").transform(x), x)

if __name__ == "__main__":
    unittest.main()
