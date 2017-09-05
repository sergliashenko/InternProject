import json
import typing

with open("resources\skills.json") as f:
    SKILLS = json.load(f)
with open("resources\key_words.json") as f:
    key_words = json.load(f)


def get_len_job_detail(json_data: dict) -> typing.Union[int, None]:
    """
    Getting numbers of symbols from job details, if Job details is empty - returning None
    :param json_data: dict. incoming data from ParserUpwork
    :return: int or None. Length of string
    """
    if "Job details" in json_data:
        return len(json_data["Job details"])
    else:
        return None


def get_posted_time(json_data: dict) -> typing.Union[float, None]:
    """
    Getting float value of posted time in days if possible, None - other wise
    :param json_data:dict,incoming data from JSON
    :return: float,None
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


def get_last_viewing(json_data: dict) -> typing.Union[float, None]:
    """
    Getting float value of last viewing by a client in days, if possible, None - other wise

    :param json_data:disc, incoming data from JSON file
    :return:float, None
    """
    if not "Activity on this Job" in json_data:
        return None
    activity_on_this_job = json_data["Activity on this Job"]
    last_viewing = None
    for i in activity_on_this_job:
        if "Last Viewed" in i:
            last_viewing = i
            break

    if last_viewing is None:
        return None

    parsed_last_viewing = last_viewing.replace("Last Viewed by Client:","").replace("ago","").strip()
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


def get_proposals(json_data: dict) -> typing.Union[list, None]:
    """
    Getting number of proposals range.
    :param json_data:dict, incoming data from JSON file.
    :return:list or None
    """
    if not "Activity on this Job" in json_data:
        return None
    activity_on_this_job = json_data["Activity on this Job"]
    proposals = None
    for i in activity_on_this_job:
        if "Proposals" in i:
            proposals = i
            break
    if proposals is None:
        return None
    parsing_proposals = proposals.replace("Proposals: ","")
    if "to" in parsing_proposals:
        result = parsing_proposals.split("to")
        return map(int, result)
    elif "+" in parsing_proposals:
        result = parsing_proposals.replace("+")
        result = [result, 9999]
        return map(int, result)


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









