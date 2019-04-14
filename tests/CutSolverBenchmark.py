import random
import time
import unittest

from model.CutSolver import _solve_bruteforce, _solve_gapfill, _solve_FFD
from model.Job import TargetSize, Job


# from tests.CutSolverBenchmark import CutSolverBenchmark
# from tests.CutSolverTest import CutSolverTest
# import cProfile
# cProfile.run(CutSolverBenchmark.test_quality())


class CutSolverBenchmark(unittest.TestCase):

    @staticmethod
    def test_benchmark():
        job = Job(length_stock=1200, target_sizes=(
            TargetSize(length=300, amount=3), TargetSize(length=200, amount=3), TargetSize(length=100, amount=3)),
                  cut_width=0)

        start = time.perf_counter()
        solved_bruteforce = _solve_bruteforce(job)
        t_bruteforce = time.perf_counter() - start
        solved_gapfill = _solve_gapfill(job)
        t_gapfill = time.perf_counter() - t_bruteforce
        solved_FFD = _solve_FFD(job)
        t_FFD = time.perf_counter() - t_gapfill

        # bruteforce should be better at the cost of increased runtime
        print(f"[Runtime] Bruteforce: {t_bruteforce:.2f}s, Gapfill: {t_gapfill:.2f}s, FFD: {t_FFD:.2f}s")

        # 10 Values (2700X):
        # Bruteforce: 20s with single-core 2700X
        # Gapfill: 0.07s

    @staticmethod
    def test_quality():
        job = random_job()

        start = time.perf_counter()
        solved_gapfill = _solve_gapfill(job)
        t_gapfill = time.perf_counter() - start
        solved_FFD = _solve_FFD(job)
        t_FFD = time.perf_counter() - t_gapfill

        print(f"[Runtime] Gapfill: {t_gapfill:.2f}s, FFD: {t_FFD:.2f}s")
        print(f"[Quality] Gapfill: {len(solved_gapfill.stocks)} stocks, FFD: {len(solved_FFD.stocks)} stocks")


def random_job() -> Job:
    length_stock = random.randint(1000, 2000)
    cut_width = random.randint(0, 10)

    n_sizes = random.randint(5, 10)

    sizes = []
    for i in range(n_sizes):
        sizes.append(TargetSize(length=random.randint(10, 1000), amount=random.randint(1, 20)))

    return Job(length_stock=length_stock, target_sizes=sizes, cut_width=cut_width)


if __name__ == '__main__':
    unittest.main()
