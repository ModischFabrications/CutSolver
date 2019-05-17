from pathlib import Path

# import from app! Modules won't be found otherwise
from app.model.Job import TargetSize, Job


def test_to_JSON():
    target = TargetSize(length=300, amount=4)
    assert target.json() == '{"length": 300, "amount": 4}'

    job = Job(length_stock=1200, target_sizes=(target, TargetSize(length=200, amount=3)), cut_width=0)
    assert job.json() == '{"length_stock": 1200, "target_sizes": [{"length": 300, "amount": 4}, ' \
                         '{"length": 200, "amount": 3}], "cut_width": 0}'


def test_from_JSON():
    json_file = Path("./tests/testjob.json")
    assert json_file.exists()

    with open(json_file, "r") as encoded_job:
        job = Job.parse_raw(encoded_job.read())
        assert job.__class__ == Job
        assert len(job) > 0
