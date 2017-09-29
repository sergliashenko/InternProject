from src import encoder

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import KFold
from sklearn.model_selection import GridSearchCV

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


def cross_validate(features: np.ndarray, labels: np.ndarray) -> None:
    rf = RandomForestClassifier(n_estimators=50, max_features="log2", random_state=50, n_jobs=-1,
                                class_weight="balanced")

    parameters_grid = {
        "n_estimators": [100, 300, 500, 700],
        "max_features": ['sqrt', 'log2'],
        "random_state": [40, 60, 80, 100]
    }

    # K-Fold cross validation
    cv = KFold(n_splits=10, shuffle=True)
    cv_rf = GridSearchCV(estimator=rf, param_grid=parameters_grid, cv=cv, verbose=1, n_jobs=-1)

    for train_idx, test_idx in cv.split(features):
        X_train, X_test = features[train_idx], features[test_idx]
        y_train, y_test = labels[train_idx], labels[test_idx]
        cv_rf.fit(X_train, y_train)
        y_pred = cv_rf.predict(X_test)

        print ("best params: ", cv_rf.best_params_)
        print ("best score: ", cv_rf.best_score_)

        print("y_test: %i\ty_pred: %i" % (sum(y_test), sum(y_pred)))
        report = classification_report(y_test, y_pred)
        print(report)


def train(features: np.ndarray, labels: np.ndarray) -> None:
    rf = RandomForestClassifier(200)

    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.33)
    rf.fit(X_train, y_train)

    y_pred = rf.predict(X_test)

    print("y_test: %i\ty_pred: %i" % (sum(y_test), sum(y_pred)))
    print(classification_report(y_test, y_pred))


if __name__ == '__main__':
    features, labels = prepare_data(r"./resources/data")
    # train(features, labels)
    cross_validate(features=features, labels=labels)
    # for i in range(5):
    #     train(features, labels)
