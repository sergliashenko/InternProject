from src import encoder

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.externals import joblib

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


def cross_validate(features: np.ndarray, labels: np.ndarray, n_folds: int=10):
    rf = RandomForestClassifier(n_jobs=-1, class_weight="balanced")
    parameters_grid = {"n_estimators": [100, 300, 500, 700],
                       "max_features": ['sqrt', 'log2']}

    cv_rf = GridSearchCV(estimator=rf, param_grid=parameters_grid, scoring="f1", cv=n_folds, verbose=2, n_jobs=-1)
    cv_rf.fit(features, labels)
    print(cv_rf.cv_results_)

    return cv_rf.best_estimator_


def train(features: np.ndarray, labels: np.ndarray, model_params):
    rf = RandomForestClassifier(**model_params)
    rf.fit(features, labels)
    return rf


def save_model(model, path):
    joblib.dump(model, path)


def load_model(path):
    return joblib.load(path)


if __name__ == '__main__':
    features, labels = prepare_data(os.path.join("resources", "data"))
    model = cross_validate(features=features, labels=labels)
    save_model(model, os.path.join("resources", "data", "model.pkl"))
