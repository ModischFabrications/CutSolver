from flask import Flask

app = Flask(__name__)


@app.route("/solve", methods=["POST"])
def solve():
    pass


@app.route("/", methods=["GET"])
def index():
    return f"Hello Flask!\n"


if __name__ == "__main__":
    app.run(host="0.0.0.0")  # host needed to be acessible from outside
