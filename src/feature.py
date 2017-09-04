import os
import json
import typing

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

def get_job_id(json_data: dict) -> str:
    return json_data.get("Job id")

def get_job_link(json_data: dict) -> str:
    return json_data.get("Job link")

def get_job_name(json_data: dict) -> str:
    return json_data.get("Job name")

def get_job_direction(json_data: dict) -> typing.Union[str,None]:
    return json_data.get("Job direction", None)

def get_posted_time(json_data: dict) -> typing.Union[float, None]:
    """
    Getting float value of posted time in days if possible, None - other wise
    :param json_data:dict,incoming data from JSON
    :return: float, NoneType
    """
    if not "Posted time" in json_data:
        return None
    posted_time = json_data["Posted time"]
    parsed_posted_time = posted_time.replace("Posted","").replace("ago","").strip()
    value, quantity = parsed_posted_time.split(" ")
    value = float(value)
    quantity = quantity.strip()
    if quantity == "hours":
        return value / 24.0
    elif quantity == "days":
        return value
    elif quantity == "months":
        return value * 30.0
    else:
        return None

def get_job_additional_info(json_data: dict) -> typing.Union[str, None]:
    return json_data.get("Additional information", None)

def get_job_details(json_data: dict) -> typing.Union[str, None]:
    return json_data.get("Job details", None)

def get_job_additional_details(json_data: dict) -> typing.Union[list, None]:
    return json_data.get("Additional_details", None)

def get_job_skills(json_data: dict) -> typing.Union[list, None]:
    """
    Getting value of field "Other Skills", if this field not exist return None
    :param json_data: dict
    :return: list or NoneType
    """
    additioanl_details = get_job_additional_details(json_data)
    if additioanl_details is None:
        return None
    for data in additioanl_details:
        if "Other Skills" in data:
            idx = data.find(":") + 1
            return(data[idx:len(data) - 1].replace('"', "").split(","))

def get_project_type(json_data: dict) ->typing.Union[str, None]:
    """
    Getting value of field "Project type", if this field not exist return None
    :param json_data: dict
    :return: str or NoneType
    """
    additioanl_details = get_job_additional_details(json_data)
    if additioanl_details is None:
        return None
    for data in additioanl_details:
        if "Project Type" in data:
            idx = data.find(":") + 1
            return (data[idx:len(data)].strip())

def get_activity_on_job(json_data: dict) -> typing.Union[list, None]:
    return json_data.get("Activity on this Job", None)

def get_client_info(json_data: dict) -> typing.Union[list, None]:
    return json_data.get("About the client", None)

def get_avg_hourly_rate(json_data: dict) -> typing.Union[float, None]:
    """
    Getting avg hourly rate if exist this field, in other case return None
    :param json_data: dict
    :return: float or NoneType
    """
    client_info = get_client_info(json_data)
    if client_info is None:
        return None
    for info in client_info:
        if "Avg Hourly Rate Paid" in info:
            idx = info.find("/hr")
            avg_hourly_rate = info[1:idx]
            return float(avg_hourly_rate)
    return None

def get_job_type(json_data: dict) -> typing.Union[str, None]:
    """
    Getting Job type if this field not exist return None
    :param json_data: dict
    :return: str(Hourly or Fixed Price) or NoneType
    """
    additional_info = get_job_additional_info(json_data)
    if additional_info is None:
        return None
    if "Hourly" in additional_info:
        return "Hourly"
    elif "Fixed Price" in additional_info:
        return "Fixed Price"
    else:
        return None

def get_client_history(json_data: dict) -> typing.Union[int, None]:
    """
    Getting count of Hires. If not exist Hires return zero
    :param json_data: dict
    :return: int or None
    """
    client_info = get_client_info(json_data)
    if client_info is None:
        return None
    for info in client_info:
        if "Total Spent" in info:
            for el in info.split():
                if el.isdigit():
                    return int(el)
    return 0

def get_value_of_hours_per_week(json_data: dict) ->typing.Union[str, None]:
    """
    Getting working time per week
    :param json_data: dict
    :return: str(Less/More than 30 hrs/week) or NoneType
    """
    additional_info = get_job_additional_info(json_data)
    if additional_info is None:
        return None
    hours_per_week_constant = ["Less than 30 hrs/week", "More than 30 hrs/week"]
    for value in hours_per_week_constant:
        if value in additional_info:
            return value
    return None

def get_project_length(json_data: dict) -> typing.Union[str, None]:
    """
    Getting duration of project
    :param json_data: dict
    :return: str or NoneType
    """
    additional_info = get_job_additional_info(json_data)
    if additional_info is None:
        return None
    project_len_constant = ["Less than 1 week", "Less than 1 month", "1 to 3 months", "3 to 6 months", "More than 3 months", "More than 6 months"]
    for len in project_len_constant:
        if len in additional_info:
            return len
    return None


def main():
    json_data = get_text_from_json_files("~01a3f9faf308d8847a.json")


if __name__ == "__main__":
    main()