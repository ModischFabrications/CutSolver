from flask import Flask, request, Response

from model.CutSolver import distribute
from model.Job import JobSchema, Job, SolvedSizesSchema

app = Flask(__name__)


@app.route("/solve", methods=["POST"])
def solve():
    job = JobSchema().loads(request.data).data

    assert job.__class__ == Job

    print(f"Got job with ID {job.get_ID()}")

    solved = distribute(job)

    # TODO: redirect(...) to /solved/<id>
    return SolvedSizesSchema().dumps(solved)


# TODO: "/solved/<id>"
# cache results in ring buffer or with max_time
# return "still calculating" for keys(ids) not in solved but in pending
# return 404 for keys not in solved or pending


@app.route("/", methods=["GET"])
def index():
    # TODO: add index
    return f"Hello Flask!\n"


@app.route("/about", methods=["GET"])
def about():
    text = 'Visit <a href="https://github.com/ModischFabrications/CutSolver">' \
           'the repository</a> for further informations.'
    resp = Response(text, status=200, mimetype="text/html")
    return resp


if __name__ == "__main__":
    app.run(host="0.0.0.0")  # host needed to be accessible from outside
