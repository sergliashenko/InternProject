from src import features


def filter_actuality_of_vacancy(json_data):
    """

    :param json_data:dict
    :return: bool
    """
    if features.get_posted_time(json_data) >= 20.0 and features.get_last_viewing(json_data) >= 15.0:
        return False
    else:
        return True


def filter_find_key_words(json_data):
    """

    :param json_data:
    :return:
    """


