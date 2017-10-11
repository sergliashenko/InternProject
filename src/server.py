import interface

from flask import Flask
from flask import request

from sklearn.externals import joblib

import os

app = Flask(__name__)


model = joblib.load(os.path.join("resources", "model.pkl"))


@app.route("/")
def hello():
    return "Hello!"


@app.route('/predict_job/<path:job_link>')
def predict_job(job_link):
    try:
        result = interface.predict_job_by_link(job_link, model)
    except Exception as e:
        print(str(e))
        result = None

    return str(result)


@app.route("/predict_direction", methods=["GET"])
def predict_direction():
    try:
        direction = request.args.get('direction')
        n = request.args.get('n')
        if n is None:
            n = 10
        else:
            n = int(n)

        result = interface.predict_job_direction(direction, model, n)
    except Exception as e:
        print(str(e))
        result = [("ERROR:", str(e))]

    s = "\r\n".join([str(r[0]) + ": " + str(r[1])for r in result])
    print(s)

    return s


app.run(port=5000)
