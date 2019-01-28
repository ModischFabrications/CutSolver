import time
import unittest

from model.CutSolver import *
from model.Job import TargetSize, Job


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

    def test_benchmark(self):
        job = Job(1200, (TargetSize(300, 4), TargetSize(200, 3), TargetSize(100, 3)), 0)

        start = time.perf_counter()
        _, trimmings_bruteforce = Solver._solve_bruteforce(job)
        t_bruteforce = time.perf_counter() - start
        _, trimmings_gapfill = Solver._solve_gapfill(job)
        t_gapfill = time.perf_counter() - t_bruteforce
        # result_FFD = Solver._solve_gapfill(job)

        # bruteforce should be better at the cost of increased runtime
        print(f"[Trimmings] Bruteforce: {trimmings_bruteforce}, Gapfill: {trimmings_gapfill}")
        print(f"[Runtime] Bruteforce: {t_bruteforce}, Gapfill: {t_gapfill}")
        self.assertGreaterEqual(trimmings_gapfill, trimmings_bruteforce)
        self.assertGreaterEqual(t_bruteforce, t_gapfill)

        # 10 Values (2700X):
        # Bruteforce: 20s with single-core 2700X
        # Gapfill: 0.07s


if __name__ == '__main__':
    unittest.main()
