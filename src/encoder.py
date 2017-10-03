from src import features

from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.preprocessing import LabelBinarizer
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

with open(os.path.join("resources", "countries.json")) as f:
    countries_encoder = LabelBinarizer()
    data = json.load(f)
    countries_encoder.fit(data)

with open(os.path.join("resources", "project_status.json")) as f:
    project_status_encoder = MultiLabelBinarizer()
    project_status_encoder.fit([json.load(f)])


def encode_job(job_desc: dict, is_labeled: bool=True) -> Tuple[np.ndarray, np.ndarray]:
    skills = skills_encoder.transform([features.get_skills(job_desc)])
    key_words = key_words_encoder.transform([features.get_key_words(job_desc)])
    country = features.get_country(job_desc)
    country = countries_encoder.transform([country]) if country is not None else np.zeros([1, 73])

    signup_date = features.get_signup_date(job_desc)
    signup_date = np.array([[signup_date.year]] if signup_date is not None else np.array([[0.0]]))

    project_status = features.get_project_status(job_desc)
    # Hardcode in "else" condition
    project_status = project_status_encoder.transform([project_status]) if project_status is not None else np.zeros([1, 13])

    job_posted = features.get_client_jobs_posted(job_desc)
    job_posted = np.array([[job_posted]]) if job_posted is not None else np.array([[0.0]])

    number_of_freelancers = features.get_n_of_freelancers(job_desc)
    number_of_freelancers = np.array([[number_of_freelancers]]) if number_of_freelancers is not None else np.array([[0.0]])

    price = features.get_fixed_price(job_desc)
    price = np.array([[price]]) if price is not None else np.array([[0.0]])

    job_type_price = ["fixed price", "hourly"]
    job_type_price_encoder = MultiLabelBinarizer()
    job_type_price_encoder.fit([job_type_price])
    fixed_or_hourly = features.get_filter_of_fixed_or_hourly(job_desc)
    fixed_or_hourly = job_type_price_encoder.transform([[fixed_or_hourly]]) if fixed_or_hourly is not None \
        else np.array([[0.0, 0.0]])

    # TODO: add other features
    # ...
    if is_labeled:
        label = 1.0 if job_desc["good"] == "+" else 0.0
    else:
        label = 0.0
    return np.concatenate([skills, key_words, country, signup_date, project_status, job_posted, number_of_freelancers,
                           price, fixed_or_hourly], axis=1), np.array([label])
