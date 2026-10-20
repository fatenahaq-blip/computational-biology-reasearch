import unittest
import numpy as np
from stage8_patient_audit import cluster_bootstrap

class TestPatientAudit(unittest.TestCase):
    def test_cluster_bootstrap_bounds(self):
        y=np.array([0,1,0,1,0,1,0,1])
        pred=np.array([0,1,0,0,0,1,0,1])
        groups=np.array(["a","a","b","b","c","c","d","d"])
        interval, n=cluster_bootstrap(y,pred,groups,n_boot=200)
        self.assertEqual(n,200)
        self.assertTrue(0 <= interval[0] <= interval[1] <= 1)

if __name__ == "__main__":
    unittest.main()
