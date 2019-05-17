from app.model.Job import Job, TargetSize


def test_job_generator():
    job = Job(length_stock=1550, target_sizes=(
        TargetSize(length=500, amount=4), TargetSize(length=200, amount=3), TargetSize(length=100, amount=2)),
              cut_width=5)

    resulting_list = []
    for length in job.get_sizes():
        resulting_list.append(length)

    assert resulting_list == [500, 500, 500, 500, 200, 200, 200, 100, 100]


def test_job_dunders():
    job1 = Job(length_stock=100, target_sizes=(TargetSize(length=100, amount=2), TargetSize(length=200, amount=1)),
               cut_width=0)
    job2 = Job(length_stock=100, target_sizes=(TargetSize(length=100, amount=2), TargetSize(length=200, amount=1)),
               cut_width=0)

    assert job1 == job2
    assert len(job1) == 3
