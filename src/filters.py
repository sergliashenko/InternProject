from src import features


def check_client_country(json_data):
    """
    If client from India, Turkey, than return True
    :param json_data: dict
    :return: bool
    """
    excluded_country = ["India", "Turkey"]
    client_info = features.get_client_info(json_data)
    if client_info is not None:
        if excluded_country in client_info:
            return True
    return False


def check_vacancies_which_only_for_registered_users(json_data):
    """
    If Access is restricted to Upwork users only, than return True
    :param json_data: dict
    :return: bool
    """
    job_name = features.get_job_name(json_data)
    if "Access is restricted to Upwork users only" in job_name:
        return True
    else:
        return False


def check_smallest_price(json_data):
    """
    If avg price per hour is very smallest then return True, in other case False
    :param json_data: dict
    :return: bool
    """
    avg_hourly_rate = features.get_avg_hourly_rate(json_data)
    if avg_hourly_rate is not None:
        if avg_hourly_rate < 3.0:
            return True
    return False


def filters(json_data):
    if check_vacancies_which_only_for_registered_users(json_data):
        return False
    if check_client_country(json_data) and check_smallest_price(json_data):
        return False
    hires = features.get_client_history(json_data)
    if hires is not None and hires == 0 and check_smallest_price(json_data):
        return False
    posted_time = features.get_posted_time(json_data)
    proposals = features.get_proposals(json_data)  # TODO need correct output from this function
    if posted_time is not None and posted_time > 3.0 and proposals == "Less than 3":
        return False
    return True


def filter_actuality_of_vacancy(json_data):
    """

    :param json_data:dict
    :return: bool
    """
    if features.get_posted_time(json_data) >= 20.0 and features.get_last_viewing(json_data) >= 15.0:
        return False
    else:
        return True
