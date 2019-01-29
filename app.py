from flask import Flask, jsonify, request

from model.CutSolver import distribute
from model.Job import JobSchema

app = Flask(__name__)


@app.route("/solve", methods=["POST"])
def solve():
    assert request.is_json

    job = JobSchema().loads(request.get_json())

    print(f"Got job with ID {job.get_ID()}")

    solved = distribute(job)

    # TODO: redirect(...) to /solved/<id>
    return jsonify(solved)


# TODO: "/solved/<id>"
# cache results in ring buffer or with max_time
# return "still calculating" for keys(ids) not in solved but in pending
# return 404 for keys not in solved or pending


@app.route("/", methods=["GET"])
def index():
    # TODO: add description and index
    return f"Hello Flask!\n"


@app.route("/about", methods=["GET"])
def about():
    return 'Visit <a href="https://github.com/ModischFabrications/CutSolver">' \
           'the repository</a> for further informations'


if __name__ == "__main__":
    app.run(host="0.0.0.0")  # host needed to be acessible from outside
