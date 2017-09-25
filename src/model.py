from src import encoder

from sklearn.svm import LinearSVC
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

                features.append(feature)
                labels.append(label)

    return np.array(features), np.array(labels)


def train(features: np.ndarray, labels: np.ndarray) -> None:
    gs = GridSearchCV(LinearSVC(dual=False), param_grid={"C": [10 * i for i in range(-5, 5)]}, cv=5)
    gs.fit(features, labels)
