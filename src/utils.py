import os
import json
import matplotlib.pyplot as plt
import numpy as np

def get_files_with_ext(path, ext="json"):
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


def fix_json(path):
    for root, dirs, files in os.walk(path):
        for f in files:
            if not f.endswith(".json"):
                os.remove(os.path.join(root, f))
                continue

            with open(os.path.join(root, f)) as ff:
                data = json.load(ff)
                if len(data) == 2:
                    data = data[1]
                else:
                    print("Wrong length: %s" % str(data))
                    continue

            if "good" in data:
                if "good" in root:
                    data["good"] = "+"
                elif "bad" in root:
                    data["good"] = "-"
                else:
                    raise ValueError("Wrong path: %s" % root)

                with open(os.path.join(root, f), "w") as ff:
                    json.dump(data, ff)
            else:
                print("No good in: %s" % os.path.join(root, f))
                os.remove(os.path.join(root, f))


def get_countries(path):
    from src.features import get_country
    json_files = get_files_with_ext(path)
    countries = []
    for f in json_files:
        with open(f, "r") as fp:
            data = json.load(fp)
            c = get_country(data)
            if c is None:
                c = "None"
            if c == "United":
                continue
            countries.append(c)
    # print(countries)
    occurences = [(x, countries.count(x)) for x in set(countries) if countries.count(x) > 10]

    print (len(occurences))
    print(occurences)
    return occurences

if __name__ == '__main__':
    countries_by_occur = get_countries("/Users/skondrat/repo/ParserUpWork/src/resources/data")
    plt.rcdefaults()
    fig, ax = plt.subplots()
    countries = [x[0] for x in countries_by_occur]
    occurs_num = [x[1] for x in countries_by_occur]
    y_pos = np.arange(len(countries))

    ax.barh(y_pos, occurs_num, align='center',
            color='green')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(countries)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('number of vacancies')
    ax.set_title('countries by occurance')

    plt.show()