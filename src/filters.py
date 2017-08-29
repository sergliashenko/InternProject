from src import feature

def filter_check_client_country(json_data):
    """
    If client from India, Turkey, than return False
    :param json_data: dict
    :return: bool
    """
    excluded_country = ["India", "Turkey"]
    client_info = feature.get_client_info(json_data)
    #TODO if country info not exist
    if excluded_country in client_info:
        return False
    else:
        return True

def filter_vacancies_which_only_for_registered_users(json_data):
    """
    If Access is restricted to Upwork users only, than return False
    :param json_data: dict
    :return: bool
    """
    job_name = feature.get_job_name(json_data)
    if "Access is restricted to Upwork users only" in job_name:
        return False
    else:
        return True

def filter_smollest_price(json_data):
    """
    If avg price per hour is very smallest then return False, in other case True
    :param json_data: dict
    :return: bool
    """
    avg_hourly_rate = feature.get_avg_hourly_rate(json_data)
    if avg_hourly_rate != None:
        if avg_hourly_rate < 3.0:
            return False
        else:
            return True
    else:
        return # TODO if avg is None
    