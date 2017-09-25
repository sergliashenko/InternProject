from src import features

from sklearn.preprocessing import MultiLabelBinarizer
import numpy as np

import os
import json
from typing import Tuple

with open(os.path.join("resources", "skills.json")) as f:
    skills_encoder = MultiLabelBinarizer()
    skills_encoder.fit(json.load(f).keys())

with open(os.path.join("resources", "key_words.json")) as f:
    key_words_encoder = MultiLabelBinarizer()
    key_words_encoder.fit(json.load(f).keys())


def encode_job(job_desc: dict) -> Tuple[np.ndarray, np.ndarray]:
    skills = skills_encoder.transform(features.get_skills(job_desc))
    key_words = key_words_encoder.transform(features.get_key_words(job_desc))

    # TODO: add other features
    # ...

    label = 1.0 if job_desc["good"] == "+" else 0.0

    return np.concatenate([skills, key_words]), np.array([label])
