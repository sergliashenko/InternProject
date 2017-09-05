import pytest

from src import features

import numpy as np
import json


def test_get_len_job_detail():
    # read json
    with open("resources/test_data.json") as f:
        json_data = json.load(f)

    # call function
    len_job_detail = features.get_len_job_detail(json_data)

    # assert
    assert len_job_detail == 1153


def test_get_posted_time():
    with open("resources/test_data.json") as f:
        json_data = json.load(f)

    posted_time = features.get_posted_time(json_data)

    assert posted_time == 270.0

    with open("resources/test_data1.json") as f:
        json_data = json.load(f)

    posted_time = features.get_posted_time(json_data)

    assert np.isclose(posted_time, 0.83, 0.01)

    with open("resources/test_data2.json") as f:
        json_data = json.load(f)

    posted_time = features.get_posted_time(json_data)

    assert posted_time == 10


def test_get_last_viewing():
    with open("resources/test_data.json") as f:
        json_data = json.load(f)
    last_viewing = features.get_last_viewing(json_data)

    assert last_viewing == 27


def test_normalise_string():

    input_value = "THIS IS TEST FOR TESTS"
    output_value = "this is test for tests"

    assert features.normalise_string(input_value) == output_value


def test_skills_from_string():

    input_value = "C++ and ruby is testing data for tests, another value is c plus plus and ruby in rails"
    output_value = ['c++', 'ruby']

    assert set(features.get_skills_from_string(input_value)) == set(output_value)


def test_skills():
    with open("resources/test_data.json") as f:
        json_data = json.load(f)

    skills = features.get_skills(json_data)

    assert skills == ['html']


def test_find_key_words():
    with open("resources/test_data.json") as f:
        json_data = json.load(f)

    find_key = features.get_find_key_words(json_data)

    assert find_key == ["bug"]