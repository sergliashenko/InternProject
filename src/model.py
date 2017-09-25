from src import encoder

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

from sklearn.ensemble import RandomForestClassifier

import numpy as np

import os
import json
from typing import Tuple


def prepare_data(path: str) -> Tuple[np.ndarray, np.ndarray]:
    features = []
    labels = []

    for root, dirs, files in os.walk(path):
        for f in files:
            if f.endswith(".json"):
                with open(os.path.join(root, f)) as ff:
                    job_desc = json.load(ff)

                feature, label = encoder.encode_job(job_desc)

                features.append(feature[0])
                labels.append(label[0])

    return np.array(features), np.array(labels)


def train(features: np.ndarray, labels: np.ndarray) -> None:
    rf = RandomForestClassifier(200)

    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.33)
    rf.fit(X_train, y_train)

    y_pred = rf.predict(X_test)

    print("y_test: %i\ty_pred: %i" % (sum(y_test), sum(y_pred)))
    print(classification_report(y_test, y_pred))


if __name__ == '__main__':
    features, labels = prepare_data(r"C:\Users\vlad\Projects\ParserUpWork\src\resources\data")
    for i in range(5):
        train(features, labels)
