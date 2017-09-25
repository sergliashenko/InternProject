from src import features

from sklearn.preprocessing import MultiLabelBinarizer
import numpy as np

import os
import json
from typing import Tuple

with open(os.path.join("resources", "skills.json")) as f:
    skills_encoder = MultiLabelBinarizer()
    skills_encoder.fit([json.load(f).keys()])

with open(os.path.join("resources", "key_words.json")) as f:
    key_words_encoder = MultiLabelBinarizer()
    key_words_encoder.fit([json.load(f).keys()])


def encode_job(job_desc: dict) -> Tuple[np.ndarray, np.ndarray]:
    skills = skills_encoder.transform([features.get_skills(job_desc)])
    key_words = key_words_encoder.transform([features.get_key_words(job_desc)])

    price = features.get_fixed_price(job_desc)
    price = np.array([[price]]) if price is not None else np.array([[0.0]])

    fixed_or_hourly = features.get_filter_of_fixed_or_hourly(job_desc)
    if fixed_or_hourly == "fixed price":
        fixed_or_hourly = np.array([[1.0, 0.0]])
    elif fixed_or_hourly == "hourly":
        fixed_or_hourly = np.array([[0.0, 1.0]])
    else:
        fixed_or_hourly = np.array([[0.0, 0.0]])

    # TODO: add other features
    # ...

    label = 1.0 if job_desc["good"] == "+" else 0.0

    return np.concatenate([skills, key_words, price, fixed_or_hourly], axis=1), np.array([label])
