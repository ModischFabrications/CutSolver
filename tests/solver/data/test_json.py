from pathlib import Path

# import from app! Modules won't be found otherwise
from app.solver.data.Job import Job, TargetSize


def test_to_json():
    job = Job(
        max_length=1200,
        cut_width=5,
        target_sizes=[
            TargetSize(length=300, quantity=4, name="Part1"),
            TargetSize(length=200, quantity=3),
        ],
    )
    assert (
        job.model_dump_json()
        == '{"max_length":1200,"cut_width":5,"target_sizes":[{"length":300,"quantity":4,"name":"Part1"},{"length":200,"quantity":3,"name":""}]}'
    )


def test_from_json():
    json_file = Path("./tests/res/in/testjob.json")
    assert json_file.exists()

    with open(json_file, "r") as encoded_job:
        job = Job.model_validate_json(encoded_job.read())
        assert job.__class__ == Job
        assert len(job) > 0
