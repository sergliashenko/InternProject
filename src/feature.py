import os
import json

# dir with .json files
DIR_PATH = ".\JSON_data/"

def find_json_file_in_dir(path):
    """
    Find all .json files in path
    :param path: type "str" path to dir with .json files
    :return: list with .json files names
    """
    files = os.listdir(path)
    # filter only .json type
    jsons = filter(lambda x: x.endswith('.json'), files)
    return jsons

def get_text_from_json_files(json_file_name):
    """
    Write all content from .json file to dict
    :param json_file_name: str
    :return: dict
    """
    with open(DIR_PATH + json_file_name, "r", encoding='utf-8') as file:
        return json.load(file)

def get_job_id(json_data):
    return json_data.get("Job id")

def get_job_link(json_data):
    return json_data.get("Job link")

def get_job_name(json_data):
    return json_data.get("Job name")

def get_job_direction(json_data):
    return json_data.get("Job direction")

def get_job_posted_time(json_data):
    return json_data.get("Posted time")

def get_job_additional_info(json_data):
    return json_data.get("Additional information")

def get_job_details(json_data):
    return json_data.get("Job details")

def get_job_additional_details(json_data):
    return json_data.get("Additional_details")

def get_job_skills(json_data):
    for data in json_data.get("Additional_details"):
        if "Other Skills" in data:
            data = data.split()
            idx = data.find(":") + 1
            return(data[idx:len(data)])
    return None

def get_activity_on_job(json_data):
    return json_data.get("Activity on this Job")

def get_client_info(json_data):
    return json_data.get("About the client")

def get_avg_hourly_rate(json_data):
    """
    Getting avg hourly rate if exist this field, in other case return None
    :param json_data: dict
    :return: float or NonTypex
    """
    client_info = get_client_info(json_data)
    for info in client_info:
        if "Avg Hourly Rate Paid" in info:
            idx = info.find("/hr")
            avg_hourly_rate = info[1:idx]
            return float(avg_hourly_rate)
    return None



def main():
    json_data = get_text_from_json_files("~01a7c003fa84239381.json")
    #avg_hourly_rate = get_avg_hourly_rate(json_data)

    pass


if __name__ == "__main__":
    main()