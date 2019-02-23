import unittest

from model import SolverStore


class MyTestCase(unittest.TestCase):
    def test_max_ID(self):
        base_ID = SolverStore.JobStorage.get_last_Job_ID()

        self.assertGreaterEqual(0, base_ID)


if __name__ == '__main__':
    unittest.main()
