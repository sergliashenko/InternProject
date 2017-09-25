import os


def get_files_with_ext(path, ext):
    ext = ext.replace(".", "")
    files = [os.path.join(root, name)
                 for root, dirs, files in os.walk(path)
                 for name in files
                 if name.endswith(("." + ext))]
    return files


def cleanup_json_name(list_of_path):
    for p in list_of_path:
        p_new = p.replace(".json (1)", ".json").replace(".json.json", ".json")
        os.rename(p, p_new)


def get_names_list(list_ot_path):
    res = []
    for p in list_ot_path:
        p = p.replace(".json", "").replace("-", "").replace(" (1)", "").split("/")[-1]
        res.append(p)
    return res


def normalise_string(string: str) -> str:
    """
    Set string to lower case and del spaces
    :param string: str
    :return: string
    """
    return string.lower().strip()
