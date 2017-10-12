import features

from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.preprocessing import LabelBinarizer
import numpy as np
from utils import normalize

import os
import json
from typing import Tuple

job_type_price = ["fixed price", "hourly"]
job_type_price_encoder = MultiLabelBinarizer()
job_type_price_encoder.fit([job_type_price])


with open(os.path.join(os.path.dirname(os.path.realpath(__file__)),os.path.join("resources", "skills.json"))) as f:
    skills_encoder = MultiLabelBinarizer()
    skills_encoder.fit([json.load(f).keys()])

with open(os.path.join(os.path.dirname(os.path.realpath(__file__)),os.path.join("resources", "key_words.json"))) as f:
    key_words_encoder = MultiLabelBinarizer()
    key_words_encoder.fit([json.load(f).keys()])

with open(os.path.join(os.path.dirname(os.path.realpath(__file__)),os.path.join("resources", "countries.json"))) as f:
    countries_encoder = LabelBinarizer()
    data = json.load(f)
    countries_encoder.fit(data)

with open(os.path.join(os.path.dirname(os.path.realpath(__file__)),os.path.join("resources", "project_status.json"))) as f:
    project_status_encoder = MultiLabelBinarizer()
    project_status_encoder.fit([json.load(f)])

with open(os.path.join(os.path.dirname(os.path.realpath(__file__)),os.path.join("resources", "words_more.json"))) as f:
    words_encoder = MultiLabelBinarizer()
    words_encoder.fit([json.load(f)])


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

    fixed_or_hourly = features.get_filter_of_fixed_or_hourly(job_desc)
    fixed_or_hourly = job_type_price_encoder.transform([[fixed_or_hourly]]) if fixed_or_hourly is not None \
        else np.array([[0.0, 0.0]])

    # TODO: add other features
    job_details = features.get_job_details_and_name(job_desc)
    if job_details is None:
        job_details = ""
    words = normalize(job_details).split()
    words = filter(lambda x: x in words_encoder.classes_, words)
    words = words_encoder.transform([words])

    if is_labeled:
        label = 1.0 if job_desc["good"] == "+" else 0.0
    else:
        label = 0.0
    return np.concatenate([skills, key_words, country, signup_date, project_status, job_posted, number_of_freelancers,
                           price, fixed_or_hourly, words], axis=1), np.array([label])


def print_features():
    feature_names = skills_encoder.classes_.tolist() + key_words_encoder.classes_.tolist() + \
                    countries_encoder.classes_.tolist() + ["signup data"] +\
                    project_status_encoder.classes_.tolist() + ["job_posted"] + ["number_of_freelancers"] + ["price"] +\
                    job_type_price_encoder.classes_.tolist() + words_encoder.classes_.tolist()
    with open("/Users/skondrat/features.txt", "w") as fp:
        fp.write("\n".join(feature_names))

if __name__ == '__main__':
    print_features()
