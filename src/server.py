import interface

from flask import Flask

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


@app.route("/predict_direction/<string:direction>")
def predict_direction(direction):
    try:
        result = interface.predict_job_direction(direction, model)
    except Exception as e:
        print(str(e))
        result = None
    return str(result)


app.run(port=5000)
