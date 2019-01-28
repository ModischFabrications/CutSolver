import unittest

from model.CutSolver import *


class CutSolverTest(unittest.TestCase):
    def test_trimmings(self):
        trimming = Solver._get_trimming(length_stock=1500, lengths=(300, 400, 600, 100), cut_width=2)

        self.assertEqual(92, trimming)

    def test_trimmings_raise(self):
        # raises Error if more stock was used than available
        with self.assertRaises(OverflowError):
            trimming = Solver._get_trimming(1500, (300, 400, 600, 200), 2)

    def test_bruteforce(self):
        job = Job(900, (TargetSize(500, 4), TargetSize(200, 3), TargetSize(100, 2)), 0)

        stock, trimmings = Solver._solve_bruteforce(job)

        self.assertEqual(500, trimmings)

    def test_gapfill(self):
        job = Job(900, (TargetSize(500, 4), TargetSize(200, 3), TargetSize(100, 2)), 0)

        result = Solver._solve_gapfill(job)

        self.assertEqual(([[500, 200, 100], [500, 200, 100], [500, 200], [500]], 800), result)

    def test_job_generator(self):
        job = Job(1550, (TargetSize(500, 4), TargetSize(200, 3), TargetSize(100, 2)), 5)

        resulting_list = []
        for length in job.get_sizes():
            resulting_list.append(length)

        self.assertEqual([500, 500, 500, 500, 200, 200, 200, 100, 100], resulting_list)

    def test_job_dunders(self):
        job1 = Job(100, (TargetSize(100, 2), TargetSize(200, 1)), 0)
        job2 = Job(100, (TargetSize(100, 2), TargetSize(200, 1)), 0)

        self.assertNotEqual(job1, job2)
        self.assertEqual(3, len(job1))


if __name__ == '__main__':
    unittest.main()
