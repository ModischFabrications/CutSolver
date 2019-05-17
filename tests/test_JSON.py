import unittest
from pathlib import Path

# import from app! Modules won't be found otherwise
from app.model.Job import TargetSize, Job


class MyTestCase(unittest.TestCase):
    def test_to_JSON(self):
        target = TargetSize(length=300, amount=4)
        self.assertEqual('{"length": 300, "amount": 4}', target.json())

        job = Job(length_stock=1200, target_sizes=(target, TargetSize(length=200, amount=3)), cut_width=0)
        self.assertEqual('{"length_stock": 1200, "target_sizes": [{"length": 300, "amount": 4}, {"length": 200, '
                         '"amount": 3}], "cut_width": 0}', job.json())

    def test_from_JSON(self):
        json_file = Path("./tests/testjob.json")
        assert json_file.exists()

        with open(json_file, "r") as encoded_job:
            job = Job.parse_raw(encoded_job.read())
            assert job.__class__ == Job


if __name__ == '__main__':
    unittest.main()
