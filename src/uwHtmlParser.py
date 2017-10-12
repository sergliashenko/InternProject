import math
import os
import json

from urllib import request
from urllib.parse import quote_plus
from bs4 import BeautifulSoup, NavigableString

MASK_URL = "https://www.upwork.com/o/jobs/browse/"
JSON_PATH = "./JSON_data/"

# NOTE: replace this parameters with ones in your browser
# COOKIE = "session_id=a74eef23d94b4b5104f924938e578d7a; device_view=full; __cfduid=df9c47403359cc0a75f6f9a44e8a070361507736897; visitor_id=62.80.165.250.1507736891534564; qt_visitor_id=62.80.165.250.1507736891534564; XSRF-TOKEN=cdfcc862899c3b73931d268cb41573db"
COOKIE = "session_id=a21348444e3a68f2c184e17e895d837c; device_view=full; __cfduid=d19f8bb6460573b987209b0871bdeb74f1507734356; visitor_id=62.80.165.250.150702888696067; qt_visitor_id=23.14.94.184.1349767611467449; XSRF-TOKEN=ad585892c50cacaa89c3a123a88245ad"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36 OPR/48.0.2685.35"


def get_html(url):
    req = request.Request(url, headers={"cookie": COOKIE, "user-agent": USER_AGENT}, unverifiable=True)
    page = request.urlopen(req)
    return page.read()


def get_jobs_count(html):
    soup = BeautifulSoup(html, "html.parser")
    var = soup.find("meta").get("content").split()
    jobs_found = 0

    for i in var:
        if i.isdigit():
            jobs_found = i
    return int(jobs_found)


def pars_skills_field(skills_data):
    start_idx = 0
    size = len(skills_data)
    skill = ""
    while start_idx != -1:
        start_idx = skills_data.find("prettyName", start_idx)
        if start_idx != -1:
            start_idx += 12  # 12 is size of string prettyName":
            while skills_data[start_idx] != "}":
                skill += skills_data[start_idx]
                start_idx += 1
            skill += ","
    return skill


def check_on_NonType(in_obj):
    if in_obj != None:
        return in_obj.text
    else:
        return ""


def parse_one_job(job_link, job_id=""):
    job_soup = BeautifulSoup(get_html(job_link), "html.parser")
    # information about job
    job_table = job_soup.find_all("div", class_="col-md-9")
    if len(job_table) != 0:
        job_title = job_table[0].text
        first_direction = job_table[1].contents[1].text
        second_direction = job_table[1].contents[3].text
        posted_time = job_table[1].contents[5].text
        some_additional_info = job_table[1].contents[7].text
        # push categories to dict
        project = {
            "Job id": job_id,
            "Job link": job_link,
            "Job name": " ".join(job_title.replace("\n", " ").split()),
            "Job direction": " ".join(first_direction.replace("\n", " ").split()) + ", " + " ".join(
                second_direction.replace("\n", " ").split()),
            "Posted time": " ".join(posted_time.replace("\n", " ").split()),
            "Additional information": " ".join(some_additional_info.replace("\n", " ").split())
        }
        for content in job_table[1].contents[9].contents:
            if content != "\n":
                if "Details" in content.text:
                    lable_info = content.find("span", class_="label label-info")
                    job_details = content.find("p", class_="break")
                    project["Job details"] = " ".join(
                        (check_on_NonType(lable_info) + check_on_NonType(job_details)).replace("\n", " ").split())
                    content_details = content.find("div", id="form")
                    if content_details is not None:
                        additional_details = []
                        for details in content_details:
                            if type(details) != NavigableString:
                                if len(details.attrs) != 0 and "data-ng-controller" in details.attrs:
                                    skills_data = details.contents[3].attrs.get("data-ng-init")
                                    skill = pars_skills_field(skills_data)
                                    additional_details.append(details.text.strip() + skill)
                                elif details.text != "":
                                    additional_details.append(details.text.strip())
                        project["Additional_details"] = additional_details
                elif "Activity on this Job" in content.text:
                    activity = []
                    cont_activity = content.contents[1].contents[1].contents
                    size_activity = len(cont_activity)
                    for i in range(3, size_activity):
                        if cont_activity[i] != "\n":
                            activity.append(" ".join(cont_activity[i].text.replace("\n", " ").split()))
                    project["Activity on this Job"] = activity
                elif "Other open jobs by this client" in content.text:
                    other_open_jobs_by_this_client = content.contents[1].contents[3].attrs.get("data-other-jobs")
                    project["Other open jobs by this client"] = other_open_jobs_by_this_client
                    # TODO
                elif "Similar Jobs on Upwork" in content.text:
                    similar_job = content.contents[1].contents[3].attrs.get("data-similar-jobs")
                    project["Similar Jobs on Upwork"] = similar_job
                    # TODO
        # information about client
        client_table = job_soup.find_all("div", class_="col-md-3")
        client_info = []
        for client_data in client_table:
            if "About the Client" in client_data.text:
                size = len(client_data)
                client_info = []
                for i in range(7, size):
                    if client_data.contents[i] != "\n":
                        client_info.append(" ".join(client_data.contents[i].text.replace("\n", " ").split()))
        project["About the client"] = client_info
    else:
        project = {
            "Job id": job_id,
            "Job link": job_link,
            "Job name": "Access is restricted to Upwork users only. "
                        "Create an Account or Sign in to view this job post"
        }

    return project


def parser_for_one_page(html):
    # find all projects
    page_soup = BeautifulSoup(html, "html.parser")
    page_table = page_soup.find("div", class_="col-sm-12 jobs-list")
    jobs_list = page_table.find_all("section", class_="job-tile")

    for job in jobs_list:
        job_id = job.get("data-key")
        job_link = "https://www.upwork.com/o/jobs/job/_" + job_id
        project = parse_one_job(job_link, job_id)
        # write data to json file

        with open(JSON_PATH + job_id + ".json", "w", encoding='utf-8') as file:
            json.dump(project, file, indent=2, ensure_ascii=False)


def parser_runner(direction):
    # create dir where will be save json file
    if not os.path.exists(JSON_PATH):
        os.mkdir(JSON_PATH)
    # direction = "Python Machine Learning"
    number_of_page = 1
    mask_str = "?q=" + direction.replace(" ", "%20")
    path = MASK_URL + str(number_of_page) + mask_str
    pages = get_jobs_count(get_html(path))
    print("Jobs found for direction: " + '"' + direction + '"' + ": " + str(pages))

    # Find count of page
    if pages % 10 != 0:
        pages //= 10
        pages += 1
    else:
        pages //= 10

    print("All pages:" + str(pages))

    for number_of_page in range(1, pages + 1):
        print("At now parse pages: " + str(number_of_page))
        parser_for_one_page(get_html(MASK_URL + str(number_of_page) + mask_str))


def parser_for_direction(direction: str, max_number_of_jobs: int=10):
    direction = direction.replace(" ", "%20")

    # quote_plus("%s?page=1&q=%s" % (MASK_URL, direction))
    #
    # mask_str = "?page=%i&q=%s" + direction.replace(" ", "%20")
    # path = MASK_URL + str(number_of_page) + mask_str
    #
    # jobs_count = get_jobs_count(get_html(path))
    # if jobs_count > max_number_of_jobs:
    #     jobs_count = max_number_of_jobs
    #
    # pages = int(math.ceil(jobs_count / 10))
    #
    # print("All pages:" + str(pages))

    job_counter = 0

    projects = []
    for number_of_page in range(1, 9999):
        print("At now parse pages: " + str(number_of_page))
        page_url = "https://www.upwork.com/o/jobs/browse/?page=%i&q=%s" % (number_of_page, direction)
        html = get_html(page_url)
        page_soup = BeautifulSoup(html, "html.parser")
        page_table = page_soup.find("div", class_="col-sm-12 jobs-list")
        jobs_list = page_table.find_all("section", class_="job-tile")
        for job in jobs_list:
            print("parsing job #%i" % job_counter)
            job_id = job.get("data-key")
            job_link = "https://www.upwork.com/o/jobs/job/_" + job_id
            projects.append({"link": job_link, "job": parse_one_job(job_link, job_id)})

            job_counter += 1

            if job_counter >= max_number_of_jobs:
                return projects
    return projects


def main():
    direction = "Python Machine Learning"
    parser_runner(direction)


if __name__ == "__main__":
    main()
