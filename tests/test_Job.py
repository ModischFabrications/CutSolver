from app.model.Job import Job, TargetSize


def test_job_generator():
    job = Job(max_length=1550, target_sizes=(
        TargetSize(length=500, quantity=4), TargetSize(length=200, quantity=3), TargetSize(length=100, quantity=2)),
              cut_width=5)

    resulting_list = []
    for length in job.get_sizes():
        resulting_list.append(length)

    assert resulting_list == [500, 500, 500, 500, 200, 200, 200, 100, 100]


def test_job_dunders():
    job1 = Job(max_length=100, target_sizes=(TargetSize(length=100, quantity=2), TargetSize(length=200, quantity=1)),
               cut_width=0)
    job2 = Job(max_length=100, target_sizes=(TargetSize(length=100, quantity=2), TargetSize(length=200, quantity=1)),
               cut_width=0)

    assert job1 == job2
    assert len(job1) == 3


def test_equal_hash():
    job1 = Job(max_length=100, target_sizes=(TargetSize(length=100, quantity=2), TargetSize(length=200, quantity=1)),
               cut_width=0)
    job2 = Job(max_length=100, target_sizes=(TargetSize(length=100, quantity=2), TargetSize(length=200, quantity=1)),
               cut_width=0)

    assert hash(job1) == hash(job2)


def test_compress():
    job = Job(max_length=100, target_sizes=(TargetSize(length=100, quantity=2), TargetSize(length=100, quantity=3)),
              cut_width=0)
    job.compress()
    compressed_job = Job(max_length=100, target_sizes=([TargetSize(length=100, quantity=5)]), cut_width=0)

    assert job == compressed_job


def test_valid():
    job1 = Job(max_length=100, target_sizes=(TargetSize(length=100, quantity=2), TargetSize(length=200, quantity=1)),
               cut_width=0)
    assert job1.valid()


def test_invalid():
    job1 = Job(max_length=0, target_sizes=(TargetSize(length=100, quantity=2), TargetSize(length=200, quantity=1)),
               cut_width=0)
    assert not job1.valid()
