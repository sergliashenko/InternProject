from flask import Flask

app = Flask(__name__)


def our_predict(value):
    return value


@app.route('/predict/<path:link>')
def predict(link):
    return our_predict(link)

app.run(debug=True, port=5000)cd 