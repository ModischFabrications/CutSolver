import time
import unittest

from model.CutSolver import _solve_bruteforce, _solve_gapfill
from model.Job import TargetSize, Job


class CutSolverTest(unittest.TestCase):

    def test_benchmark(self):
        job = Job(length_stock=1200, target_sizes=(
        TargetSize(length=300, amount=3), TargetSize(length=200, amount=3), TargetSize(length=100, amount=3)),
                  cut_width=0)

        start = time.perf_counter()
        solved_bruteforce = _solve_bruteforce(job)
        t_bruteforce = time.perf_counter() - start
        solved_gapfill = _solve_gapfill(job)
        t_gapfill = time.perf_counter() - t_bruteforce
        # result_FFD = Solver._solve_gapfill(job)

        # bruteforce should be better at the cost of increased runtime
        print(f"[Trimmings] Bruteforce: {solved_bruteforce.trimmings}, Gapfill: {solved_gapfill.trimmings}")
        print(f"[Runtime] Bruteforce: {t_bruteforce:.2f}s, Gapfill: {t_gapfill:.2f}s")
        self.assertGreaterEqual(solved_gapfill.trimmings, solved_bruteforce.trimmings)

        # 10 Values (2700X):
        # Bruteforce: 20s with single-core 2700X
        # Gapfill: 0.07s

    def test_quality(self):
        # ToDo: generate random jobs and compare trimmings of different algorithms
        pass


if __name__ == '__main__':
    unittest.main()
