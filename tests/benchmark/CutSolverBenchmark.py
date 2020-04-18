import random
import time
import unittest

from app.solver.data.Job import TargetSize, Job
from app.solver.solver import _solve_bruteforce, _solve_gapfill, _solve_FFD


# from tests.CutSolverBenchmark import CutSolverBenchmark
# from tests.CutSolverTest import CutSolverTest
# import cProfile
# cProfile.run(CutSolverBenchmark.test_quality())


class CutSolverBenchmark(unittest.TestCase):

    @staticmethod
    def test_benchmark():
        job = Job(max_length=1200, target_sizes=(
            TargetSize(length=300, quantity=3), TargetSize(length=200, quantity=3), TargetSize(length=100, quantity=3)),
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
        print(f"[Quality] Gapfill: {len(solved_gapfill.lengths)} stocks, FFD: {len(solved_FFD.lengths)} stocks")


def random_job() -> Job:
    max_length = random.randint(1000, 2000)
    cut_width = random.randint(0, 10)

    n_sizes = random.randint(5, 10)

    sizes = []
    for i in range(n_sizes):
        sizes.append(TargetSize(length=random.randint(10, 1000), quantity=random.randint(1, 20)))

    return Job(max_length=max_length, target_sizes=sizes, cut_width=cut_width)


if __name__ == '__main__':
    unittest.main()
