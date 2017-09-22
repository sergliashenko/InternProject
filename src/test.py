import json
import numpy as np
from src import features
from datetime import datetime


def read_json_file(path):
    with open(path) as file:
        return json.load(file)


def test_get_len_job_detail():
    # read json
    json_data = read_json_file("resources/test_data.json")
    # call function
    len_job_detail = features.get_len_job_detail(json_data)
    # assert
    assert len_job_detail == 1153


def test_get_proposals():
    json_data = read_json_file("resources/test_data.json")
    proposals = features.get_proposals(json_data)

    assert proposals == [10, 50]


def test_get_posted_time():
    json_data = read_json_file("resources/test_data.json")
    posted_time = features.get_posted_time(json_data)

    assert posted_time == 270.0

    json_data = read_json_file("resources/test_data1.json")
    posted_time = features.get_posted_time(json_data)

    assert np.isclose([posted_time], [0.83], 0.01)

    json_data = read_json_file("resources/test_data2.json")
    posted_time = features.get_posted_time(json_data)

    assert posted_time == 10


def test_get_last_viewing():
    json_data = read_json_file("resources/test_data.json")
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
    json_data = read_json_file("resources/test_data.json")
    skills = features.get_skills(json_data)

    assert set(skills) == {'html', 'full stack'}


def test_find_key_words():
    json_data = read_json_file("resources/test_data.json")
    find_key = features.get_find_key_words(json_data)

    assert find_key == ["bug"]


def test_get_job_id_positive():
    json_data = read_json_file("resources/test_vacancy.json")
    # call function
    actual_id = features.get_job_id(json_data)
    # assert
    expected_id = "~01a98cdf8c74d3cbc7"
    assert actual_id == expected_id


def test_get_job_link_positive():
    json_data = read_json_file("resources/test_vacancy.json")
    # call function
    actual_link = features.get_job_link(json_data)
    expected_link = "https://www.upwork.com/o/jobs/job/_~01a98cdf8c74d3cbc7"
    assert actual_link == expected_link


def test_get_job_name_positive():
    json_data = read_json_file("resources/test_vacancy.json")
    # call function
    actual_name = features.get_job_name(json_data)
    expected_name = "Algorithmic Trading Programmer"
    assert actual_name == expected_name


def test_get_job_direction_positive():
    json_data = read_json_file("resources/test_vacancy.json")
    # call function
    actual_direction = features.get_job_direction(json_data)
    expected_direction = "Data Science & Analytics, Machine Learning"
    assert actual_direction == expected_direction


def test_get_posted_time_positive():
    json_data = read_json_file("resources/test_vacancy.json")
    # call function
    actual_posted_time = features.get_posted_time(json_data)
    expected_posted_time = 4
    assert actual_posted_time == expected_posted_time


def test_get_additional_info_positive():
    json_data = read_json_file("resources/test_vacancy.json")
    # call function
    actual_additional_info = features.get_job_additional_info(json_data)
    expected_additional_info = "Hourly More than 30 hrs/week More than 6 months " \
                               "$$ Intermediate Level Start Date August 28, 2017"
    assert actual_additional_info == expected_additional_info


def test_get_job_details_positive():
    json_data = read_json_file("resources/test_vacancy.json")
    # call function
    actual_details = features.get_job_details(json_data)
    expected_details = "Needs to hire 8 Freelancers " \
                       "Looking for a programmer who has experience in algorithmic trading. " \
                       "With specific knowledge about cryptocurrency. " \
                       "You should have knowledge of the Bittrex APIs and/or other Cryptocurrency exchanges."
    assert actual_details == expected_details


def test_get_additional_details_positive():
    json_data = read_json_file("resources/test_vacancy.json")
    # call function
    actual_additional_details = features.get_job_additional_details(json_data)
    expected_additional_details = [
        "Project Type: Ongoing project",
        "Other Skills:\"Algorithm Development\",\"Python\","
    ]
    assert actual_additional_details == expected_additional_details


def test_get_field_other_skills_positive():
    json_data = read_json_file("resources/test_vacancy.json")
    # call function
    actual_skills = features.get_field_other_skills(json_data)
    expected_skills = ["Algorithm Development", "Python"]
    assert actual_skills == expected_skills


def test_get_project_type_positive():
    json_data = read_json_file("resources/test_vacancy.json")
    # call function
    actual_project_type = features.get_project_type(json_data)
    expected_project_type = "Ongoing project"
    assert actual_project_type == expected_project_type


def test_get_activity_on_job_positive():
    json_data = read_json_file("resources/test_vacancy.json")
    # call function
    actual_activity = features.get_activity_on_job(json_data)
    expected_activity = [
        "Proposals: 5 to 10",
        "Last Viewed by Client: 1 day ago",
        "Interviewing: 1",
        "Invites Sent: 1",
        "Unanswered Invites: 0"
    ]
    assert actual_activity == expected_activity


def test_get_client_info_positive():
    json_data = read_json_file("resources/test_vacancy.json")
    # call function
    actual_client_info = features.get_client_info(json_data)
    expected_client_info = [
        "(4.91) 130 reviews",
        "United States New York 04:45 PM",
        "158 Jobs Posted 58% Hire Rate, 6 Open Jobs",
        "Total Spent 194 Hires, 3 Active",
        "$4.86/hr Avg Hourly Rate Paid 4,828 Hours",
        "Member Since Feb 19, 2012"
    ]
    assert actual_client_info == expected_client_info


def test_get_avg_hourly_rate_positive():
    json_data = read_json_file("resources/test_vacancy.json")
    # call function
    actual_avg_hourly_rate = features.get_avg_hourly_rate(json_data)
    expected_avg_hourly_rate = 4.86
    assert actual_avg_hourly_rate == expected_avg_hourly_rate


def test_get_fixed_or_hourly_positive():
    json_data = read_json_file("resources/test_vacancy.json")
    # call function
    actual_job_type = features.get_fixed_or_hourly(json_data)
    expected_job_type = "Hourly"
    assert actual_job_type == expected_job_type


def test_get_hired_by_the_client_positive():
    json_data = read_json_file("resources/test_vacancy.json")
    # call function
    actual_client_history = features.get_hired_by_the_client(json_data)
    expected_client_history = 194
    assert actual_client_history == expected_client_history


def test_get_value_of_hours_per_week_positive():
    json_data = read_json_file("resources/test_vacancy.json")
    # call function
    actual_value_of_hours_per_week = features.get_value_of_hours_per_week(json_data)
    expected_value_of_hours_per_week = "More than 30 hrs/week"
    assert actual_value_of_hours_per_week == expected_value_of_hours_per_week


def test_get_project_length_positive():
    json_data = read_json_file("resources/test_vacancy.json")
    # call function
    actual_project_length = features.get_project_length(json_data)
    expected_project_length = "More than 6 months"
    assert actual_project_length == expected_project_length


def test_get_n_of_freelancers_positive():
    json_data = read_json_file("resources/test_vacancy.json")
    # call function
    actual_count = features.get_n_of_freelancers(json_data)
    expected_count = 8
    assert actual_count == expected_count


def test_get_country_positive():
    json_data = read_json_file("resources/test_vacancy.json")
    # call function
    actual_country = features.get_country(json_data)
    expected_country = "United States New York"
    assert actual_country == expected_country


def test_get_signup_date_positive():
    json_data = read_json_file("resources/test_vacancy.json")
    # call function
    actual_signup_date = features.get_signup_date(json_data)
    expected_signup_date = datetime.strptime("2012-02-19", '%Y-%m-%d').date()
    assert actual_signup_date == expected_signup_date


def test_get_client_jobs_posted_positive():
    json_data = read_json_file("resources/test_vacancy.json")
    # call function
    actual_job_posted = features.get_client_jobs_posted(json_data)
    expected_job_posted = 158
    assert actual_job_posted == expected_job_posted
