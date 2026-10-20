import unittest
from cross_cohort_microarray import label_and_group

class TestCohortFiltering(unittest.TestCase):
    def test_training_paired_patient_ids(self):
        self.assertEqual(label_and_group("GSE10072", "GSM1", "Lung Tumor_GT00006"), (1, "GT00006"))
        self.assertEqual(label_and_group("GSE10072", "GSM2", "Normal Lung_GT00006"), (0, "GT00006"))
    def test_external_patient_pair(self):
        self.assertEqual(label_and_group("GSE7670", "GSM1", "1N: Adjacent normal part of adenocarcinoma"), (0, "PAT1"))
        self.assertEqual(label_and_group("GSE7670", "GSM2", "1T: Tumor part of adenocarcinoma"), (1, "PAT1"))
    def test_exclude_cell_lines_and_other_tumors(self):
        self.assertIsNone(label_and_group("GSE7670", "GSM3", "A549: Carcinomatoma"))
        self.assertIsNone(label_and_group("GSE7670", "GSM4", "19T: Tumor part of large cell lung cancer"))
        self.assertIsNone(label_and_group("GSE7670", "GSM5", "Adj. N. mixture: Adjacent normal part of adenocarcinoma"))

if __name__ == "__main__":
    unittest.main()
