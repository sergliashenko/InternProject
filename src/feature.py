import os
import json

# dir with .json files
DIR_PATH = ".\JSON_data/"

def find_json_file_in_dir(path):
    """
    :param path: type "str" path to dir with .json files
    :return: type "list" with .json files names
    """
    files = os.listdir(path)
    # filter only .json type
    jsons = filter(lambda x: x.endswith('.json'), files)
    return jsons

def get_text_from_json_files(json_file_name):
    """
    :param json_file_name: type "list"
    :return: type "dict"
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
        else:
            return("In this vacancy, the field of skills is empty")

def get_activity_on_job(json_data):
    return json_data.get("Activity on this Job")

def get_client_info(json_data):
    return json_data.get("About the client")




def main():
    json_data = get_text_from_json_files("~01a3f9faf308d8847a.json")
    id = get_job_skills(json_data)

    pass


if __name__ == "__main__":
    main()