import unittest
from stage7_third_cohort import parse_locked_title, wilson_interval

class TestLockedThirdCohort(unittest.TestCase):
    def test_tumor_title(self):
        self.assertEqual(parse_locked_title("3L(A)"), (1, "3"))
    def test_normal_title(self):
        self.assertEqual(parse_locked_title("7NL(A)"), (0, "7"))
    def test_reject_unrecognized(self):
        with self.assertRaises(ValueError):
            parse_locked_title("A549 cell line")
    def test_wilson_bounds(self):
        lo, hi = wilson_interval(23, 30)
        self.assertTrue(0 <= lo <= 23 / 30 <= hi <= 1)

if __name__ == "__main__":
    unittest.main()
