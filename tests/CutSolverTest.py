import unittest
from model import CutSolver


class MyTestCase(unittest.TestCase):
    def test_trimmings(self):
        trimming = CutSolver.Solver._get_trimming(length_stock=1500, lengths=(300, 400, 600, 100), cut_width=2)

        self.assertEqual(92, trimming)

    def test_trimmings_raise(self):
        with self.assertRaises(OverflowError):
            trimming = CutSolver.Solver._get_trimming(length_stock=1500, lengths=(300, 400, 600, 200), cut_width=2)


if __name__ == '__main__':
    unittest.main()
