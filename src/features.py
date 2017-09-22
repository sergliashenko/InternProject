import os
import json
import typing
from datetime import datetime, date
from fuzzywuzzy import fuzz

# dir with .json files
DIR_PATH = ".\JSON_data/"

with open("resources\skills.json") as f:
    SKILLS = json.load(f)
with open("resources\key_words.json") as f:
    key_words = json.load(f)


def get_len_job_detail(json_data: dict) -> typing.Optional[int]:
    """
    Getting numbers of symbols from job details, if Job details is empty - returning None
    :param json_data: dict. incoming data from ParserUpwork
    :return: int or None. Length of string
    """
    if "Job details" in json_data:
        return len(json_data["Job details"])
    else:
        return None


def get_posted_time(json_data: dict) -> typing.Optional[float]:
    """
    Getting float value of posted time in days if possible, None - other wise
    :param json_data:dict,incoming data from JSON
    :return: float,None
    """
    if "Posted time" not in json_data:
        return None
    posted_time = json_data["Posted time"]
    parsed_posted_time = posted_time.replace("Posted", "").replace("ago", "").strip()
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


def get_last_viewing(json_data: dict) -> typing.Optional[float]:
    """
    Getting float value of last viewing by a client in days, if possible, None - other wise

    :param json_data:disc, incoming data from JSON file
    :return:float, None
    """
    if "Activity on this Job" not in json_data:
        return None
    activity_on_this_job = json_data["Activity on this Job"]
    last_viewing = None
    for i in activity_on_this_job:
        if "Last Viewed" in i:
            last_viewing = i
            break
    if last_viewing is None:
        return None

    parsed_last_viewing = last_viewing.replace("Last Viewed by Client:", "").replace("ago", "").strip()
    value, quantity = parsed_last_viewing.split(" ")
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


def get_proposals(json_data: dict) -> typing.Optional[list]:
    """
    Getting number of proposals range.
    :param json_data:dict, incoming data from JSON file.
    :return:list or None
    """
    if "Activity on this Job" not in json_data:
        return None
    activity_on_this_job = json_data["Activity on this Job"]
    proposals = None
    for i in activity_on_this_job:
        if "Proposals" in i:
            proposals = i
            break
    if proposals is None:
        return None
    parsing_proposals = proposals.replace("Proposals: ", "")
    if "to" in parsing_proposals:
        result = parsing_proposals.split("to")
        return list(map(int, result))
    elif "+" in parsing_proposals:
        result = parsing_proposals.replace("+")
        result = [result, 9999]
        return list(map(int, result))


def get_skills(json_data: dict) -> list:
    """
    Checking for key values (from SKILLS.json) in any json file
    :param json_data:dict, incoming data from json file
    :return:list
    """
    result = []
    for key, value in json_data.items():
        if type(value) is str:
            result.extend(get_skills_from_string(value))
        if type(value) is list:
            for list_value in value:
                result.extend(get_skills_from_string(list_value))
    return list(set(result))


def get_skills_from_string(string: str) -> list:
    """
    Parsting one string for skills
    :param string: str
    :return:list
    """
    string = normalise_string(string)
    result = []
    for key in SKILLS:
        values = SKILLS[key]
        for i in values:
            if i in string:
                result.append(key)
    return result


def normalise_string(string: str) -> str:
    """
    Set string to lower case
    :param string: str
    :return: string
    """
    return string.lower()


def get_find_key_words(json_data: dict) -> list:
    """
    Finding key words in key_words.json and load it to list
    :param json_data: dict
    :return: list
    """
    result = []
    for key, value in json_data.items():
        if type(value) is str:
            result.extend(get_key_words_from_string(value))
        if type(value) is list:
            for list_value in value:
                result.extend(get_key_words_from_string(list_value))
    return list(set(result))


def get_key_words_from_string(string: str) -> list:
    """
    Parsing string and load it to list
    :return: list
    """
    string = normalise_string(string)
    result = []
    for key in key_words:
        values = key_words[key]
        for i in values:
            if i in string:
                result.append(key)
    return result


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


def get_job_direction(json_data: dict) -> typing.Optional[str]:
    return json_data.get("Job direction", None)


def get_job_additional_info(json_data: dict) -> typing.Optional[str]:
    return json_data.get("Additional information", None)


def get_job_details(json_data: dict) -> typing.Optional[str]:
    return json_data.get("Job details", None)


def get_job_additional_details(json_data: dict) -> typing.Optional[list]:
    return json_data.get("Additional_details", None)


def get_activity_on_job(json_data: dict) -> typing.Optional[list]:
    return json_data.get("Activity on this Job", None)


def get_client_info(json_data: dict) -> typing.Optional[list]:
    return json_data.get("About the client", None)


def get_field_other_skills(json_data: dict) -> typing.Optional[list]:
    """
    Getting value of field "Other Skills", if this field not exist return None
    :param json_data: dict
    :return: list or NoneType
    """
    additional_details = get_job_additional_details(json_data)
    if additional_details is None:
        return None
    for data in additional_details:
        if "Other Skills" in data:
            idx = data.find(":") + 1
            return data[idx:len(data) - 1].replace('"', "").split(",")


def get_project_type(json_data: dict) -> typing.Optional[str]:
    """
    Getting value of field "Project type", if this field not exist return None
    :param json_data: dict
    :return: str or NoneType
    """
    additional_details = get_job_additional_details(json_data)
    if additional_details is None:
        return None
    for data in additional_details:
        if "Project Type" in data:
            idx = data.find(":") + 1
            return data[idx:len(data)].strip()


def get_avg_hourly_rate(json_data: dict) -> typing.Optional[float]:
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


def get_fixed_or_hourly(json_data: dict) -> typing.Optional[str]:
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


def get_hired_by_the_client(json_data: dict) -> typing.Optional[int]:
    """
    Getting count of Hires. If not exist Hires return 0
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


def get_value_of_hours_per_week(json_data: dict) -> typing.Optional[str]:
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


def get_project_length(json_data: dict) -> typing.Optional[str]:
    """
    Getting duration of project
    :param json_data: dict
    :return: str or NoneType
    """
    additional_info = get_job_additional_info(json_data)
    if additional_info is None:
        return None
    project_len_constant = ["Less than 1 week", "Less than 1 month", "1 to 3 months", "3 to 6 months",
                            "More than 3 months", "More than 6 months"]
    for size in project_len_constant:
        if size in additional_info:
            return size
    return None


def get_n_of_freelancers(json_data: dict) -> typing.Optional[int]:
    """
    Getting value from field for example "Needs to hire 2 Freelancers" from Job details
    This field not always specified in this case return 1
    :param json_data: dict
    :return: int or NoneType
    """
    job_details = get_job_details(json_data)
    if job_details is None:
        return None
    find_str_const = "Needs to hire"
    start_pos = job_details.find(find_str_const)
    if start_pos != -1:
        end_pos = job_details.find("Freelancers")
        str_value = job_details[len(find_str_const): end_pos]
        return int(str_value)
    return 1


def get_country(json_data: dict) -> typing.Optional[str]:
    """
    Getting customer's country. If this info not identified - return None
    :param json_data: dict
    :return: str or NoneType
    """
    client_info = get_client_info(json_data)
    if client_info is None:
        return None
    for info in client_info:
        if "AM" in info or "PM" in info:
            # For example " 00:00 AM" size of this string is 9. We cut this from info
            country = info[:-9]
            return "".join(country)
    return None


def get_signup_date(json_data: dict) -> typing.Optional[date]:
    """
    Getting client's registered date in format "year-month-day"
    :param json_data: dict
    :return: date or NoneType
    """
    client_info = get_client_info(json_data)
    if client_info is None:
        return None
    find_const = "Member Since"
    for info in client_info:
        if find_const in info:
            info = info.replace(find_const, "").strip()
            d = datetime.strptime(info, '%b %d, %Y')
            return d.date()
    return None


def get_client_jobs_posted(json_data: dict) -> typing.Optional[int]:
    """
    Getting number of Jobs Posted by the client
    :param json_data: dict
    :return: int or NoneType
    """
    client_info = get_client_info(json_data)
    if client_info is None:
        return None
    find_str_const_first = "Job Posted"
    find_str_const_second = "Jobs Posted"
    for info in client_info:
        tmp = info.find(find_str_const_first)
        if tmp == -1:
            idx = info.find(find_str_const_second)
        else:
            idx = tmp
        if idx != -1:
            jobs_posted = info[:idx].strip()
            return int(jobs_posted)
    return None


def get_project_status(json_data: dict) -> typing.Optional[typing.List[str]]:
    """
    Getting project status.
    !!At now this function return word from KEY_WORDS which was found in vacancies
    :param json_data: dict
    :return: list[str] or NoneType
    """
    KEY_WORDS = ["bug", "fixing", "trouble", "shoot", "existing", "redesign", "refactoring", "ongoing", "long term",
                 "long time", "review (the) code", "maintain", "growing (team)"]
    job_details = get_job_details(json_data)
    if job_details is None:
        return None
    output_list = []
    job_details_list = job_details.split()
    for word in job_details_list:
        for key_word in KEY_WORDS:
            ratio_value = fuzz.ratio(word.lower(), key_word)
            #exept "design" because design == redesign as 86%
            if ratio_value > 83 and word.lower() != "design":
                output_list.append("In Job details: " + word + " In Keywords: " + key_word + " %" + str(ratio_value))
    return output_list


def main():
    json_data = get_text_from_json_files("~01a8f1fb6888561cd5.json")


if __name__ == "__main__":
    main()
