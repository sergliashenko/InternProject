from src import feature

def check_client_country(json_data):
    """
    If client from India, Turkey, than return True
    :param json_data: dict
    :return: bool
    """
    excluded_country = ["India", "Turkey"]
    client_info = feature.get_client_info(json_data)
    if client_info != None:
        if excluded_country in client_info:
            return True
    return False

def check_vacancies_which_only_for_registered_users(json_data):
    """
    If Access is restricted to Upwork users only, than return True
    :param json_data: dict
    :return: bool
    """
    job_name = feature.get_job_name(json_data)
    if "Access is restricted to Upwork users only" in job_name:
        return True
    else:
        return False

def check_smollest_price(json_data):
    """
    If avg price per hour is very smallest then return True, in other case False
    :param json_data: dict
    :return: bool
    """
    avg_hourly_rate = feature.get_avg_hourly_rate(json_data)
    if avg_hourly_rate != None:
        if avg_hourly_rate < 3.0:
            return True
    return False

def filter(json_data):
    if check_vacancies_which_only_for_registered_users(json_data):
        return False
    if check_client_country(json_data) and check_smollest_price(json_data):
        return False
    hires = feature.get_client_history(json_data)
    if hires != None and hires == 0 and check_smollest_price(json_data):
        return False
    posted_time = feature.get_job_posted_time(json_data)
    #TODO expected function get_proposals from Vitalik
    proposals = 0
    if posted_time != None and posted_time > 3.0 and proposals == "Less than 3":
        return False
    return True


