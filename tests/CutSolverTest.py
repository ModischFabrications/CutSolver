import time
import unittest
from pathlib import Path

from model.CutSolver import _get_trimming, _solve_bruteforce, _solve_gapfill
from model.Job import TargetSize, Job, JobSchema, TargetSizeSchema, SolvedSizesSchema


class CutSolverTest(unittest.TestCase):
    def test_trimmings(self):
        trimming = _get_trimming(length_stock=1500, lengths=(300, 400, 600, 100), cut_width=2)

        self.assertEqual(92, trimming)

    def test_trimmings_raise(self):
        # raises Error if more stock was used than available
        with self.assertRaises(OverflowError):
            trimming = _get_trimming(1500, (300, 400, 600, 200), 2)

    def test_bruteforce(self):
        job = Job(900, (TargetSize(500, 2), TargetSize(200, 3), TargetSize(100, 2)), 0)

        solved = _solve_bruteforce(job)

        self.assertEqual(0, solved.trimmings)

    def test_gapfill(self):
        job = Job(900, (TargetSize(500, 2), TargetSize(200, 3), TargetSize(100, 2)), 0)

        solved = _solve_gapfill(job)

        self.assertEqual(900, solved.trimmings)

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
        job = Job(1200, (TargetSize(300, 3), TargetSize(200, 3), TargetSize(100, 3)), 0)

        start = time.perf_counter()
        solved_bruteforce = _solve_bruteforce(job)
        t_bruteforce = time.perf_counter() - start
        solved_gapfill = _solve_gapfill(job)
        t_gapfill = time.perf_counter() - t_bruteforce
        # result_FFD = Solver._solve_gapfill(job)

        # bruteforce should be better at the cost of increased runtime
        print(f"[Trimmings] Bruteforce: {solved_bruteforce.trimmings}, Gapfill: {solved_gapfill.trimmings}")
        print(f"[Runtime] Bruteforce: {t_bruteforce}, Gapfill: {t_gapfill}")
        self.assertGreaterEqual(solved_gapfill.trimmings, solved_bruteforce.trimmings)

        # 10 Values (2700X):
        # Bruteforce: 20s with single-core 2700X
        # Gapfill: 0.07s

    def test_to_JSON(self):
        target = TargetSize(300, 4)
        target_schema = TargetSizeSchema()
        encoded_target = target_schema.dumps(target)

        job = Job(1200, (target, TargetSize(200, 3), TargetSize(100, 3)), 0)
        job_schema = JobSchema()
        encoded_job = job_schema.dumps(job)

    def test_from_JSON(self):
        json_file = Path("testjob.json")
        assert json_file.exists()

        with open(json_file, "r") as encoded_job:
            job = JobSchema().loads(encoded_job.read())

    def test_full_model(self):
        json_file = Path("testjob.json")
        assert json_file.exists()

        with open(json_file, "r") as encoded_job:
            job = JobSchema().loads(encoded_job.read())

            solved = _solve_gapfill(job.data)

            encoded_solved = SolvedSizesSchema().dumps(solved)
            self.assertGreater(20, len(encoded_solved))


if __name__ == '__main__':
    unittest.main()
