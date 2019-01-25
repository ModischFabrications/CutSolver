import unittest

from model.CutSolver import *


class CutSolverTest(unittest.TestCase):
    def test_trimmings(self):
        trimming = Solver._get_trimming(length_stock=1500, lengths=(300, 400, 600, 100), cut_width=2)

        self.assertEqual(92, trimming)

    def test_trimmings_raise(self):
        with self.assertRaises(OverflowError):
            trimming = Solver._get_trimming(1500, (300, 400, 600, 200), 2)

    def test_heuristic(self):
        Solver.n_max_precise = 0

        job = Job(1550, (TargetSize(500, 4), TargetSize(200, 3), TargetSize(100, 7)), 5)

        result = Solver.distribute(job)

        self.assertEqual((450, 234), result)


if __name__ == '__main__':
    unittest.main()
