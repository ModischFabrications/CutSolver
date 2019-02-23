import unittest

from model import SolverStore
from model.Job import Job, TargetSize


class MyTestCase(unittest.TestCase):
    def test_get_ID(self):
        base_ID = SolverStore.get_ID()

        self.assertLessEqual(0, base_ID)

    def test_set_ID(self):
        base_ID = SolverStore.get_ID()

        SolverStore.set_ID(base_ID + 1)

        self.assertEqual(base_ID + 1, SolverStore.get_ID())

    def test_continuous(self):
        SolverStore.reset_ID()
        Job._current_id = 0

        for i in range(100):
            job = Job(100, (TargetSize(100, 2), TargetSize(200, 1)), 0)
            self.assertEqual(i, job.get_ID())


if __name__ == '__main__':
    unittest.main()
