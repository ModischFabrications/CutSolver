import unittest
from pathlib import Path

from model.CutSolver import _get_trimming, _solve_bruteforce, _solve_gapfill
from model.Job import TargetSize, Job


class CutSolverTest(unittest.TestCase):
    def test_trimmings(self):
        trimming = _get_trimming(length_stock=1500, lengths=(300, 400, 600, 100), cut_width=2)

        self.assertEqual(92, trimming)

    def test_trimmings_raise(self):
        # raises Error if more stock was used than available
        with self.assertRaises(OverflowError):
            trimming = _get_trimming(1500, (300, 400, 600, 200), 2)

    def test_bruteforce(self):
        job = Job(length_stock=900, target_sizes=(
        TargetSize(length=500, amount=2), TargetSize(length=200, amount=3), TargetSize(length=100, amount=2)),
                  cut_width=0)

        solved = _solve_bruteforce(job)

        self.assertEqual(0, solved.trimmings)

    def test_gapfill(self):
        job = Job(length_stock=900, target_sizes=(
        TargetSize(length=500, amount=2), TargetSize(length=200, amount=3), TargetSize(length=100, amount=2)),
                  cut_width=0)

        solved = _solve_gapfill(job)

        self.assertEqual(900, solved.trimmings)

    def test_job_generator(self):
        job = Job(length_stock=1550, target_sizes=(
        TargetSize(length=500, amount=4), TargetSize(length=200, amount=3), TargetSize(length=100, amount=2)),
                  cut_width=5)

        resulting_list = []
        for length in job.get_sizes():
            resulting_list.append(length)

        self.assertEqual([500, 500, 500, 500, 200, 200, 200, 100, 100], resulting_list)

    def test_job_dunders(self):
        job1 = Job(length_stock=100, target_sizes=(TargetSize(length=100, amount=2), TargetSize(length=200, amount=1)),
                   cut_width=0)
        job2 = Job(length_stock=100, target_sizes=(TargetSize(length=100, amount=2), TargetSize(length=200, amount=1)),
                   cut_width=0)

        self.assertEqual(job1, job2)
        self.assertEqual(3, len(job1))

    def test_full_model(self):
        json_file = Path("testjob.json")
        assert json_file.exists()

        with open(json_file, "r") as encoded_job:
            job = Job.parse_raw(encoded_job.read())

            solved = _solve_gapfill(job)

            encoded_solved = solved.json()
            self.assertLess(20, len(encoded_solved))


if __name__ == '__main__':
    unittest.main()
