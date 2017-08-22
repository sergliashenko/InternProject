import urllib.request
import json
import os
from bs4 import BeautifulSoup

MASK_URL = "https://www.upwork.com/o/jobs/browse/?page="
JSON_PATH = "./JSON_data/"

def get_html(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'}, unverifiable=True)
    page = urllib.request.urlopen(req)
    return page.read()

def get_jobs_count(html):
    soup = BeautifulSoup(html, "html.parser")
    var = soup.find("meta").get("content").split()
    jobs_found = 0

    for i in var:
        if i.isdigit():
            jobs_found = i
    return int(jobs_found)

def parser_for_one_page(html):
    #find all projects
    page_soup = BeautifulSoup(html, "html.parser")
    page_table = page_soup.find("div", class_="col-sm-12 jobs-list")
    jobs_list = page_table.find_all("section", class_="job-tile")

    for job in jobs_list:
        job_id = job.get("data-key")
        job_link = "https://www.upwork.com/o/jobs/job/_" + job_id
        job_soup = BeautifulSoup(get_html(job_link), "html.parser")
        #information about job
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
                "Job direction": " ".join(first_direction.replace("\n", " ").split()) + ", " + " ".join(second_direction.replace("\n", " ").split()),
                "Posted time": " ".join(posted_time.replace("\n", " ").split()),
                "Additional information": " ".join(some_additional_info.replace("\n", " ").split())
            }
            for content in job_table[1].contents[9].contents:
                if content != "\n":
                    if "Details" in content.text:
                        project["Job details"] = " ".join(content.text.replace("\n", " ").split())
                    elif "Activity on this Job" in content.text:
                        activity = []
                        cont_activity = content.contents[1].contents[1].contents
                        size_activity = len(cont_activity)
                        for i in range(3,size_activity):
                            if cont_activity[i] != "\n":
                                activity.append(" ".join(cont_activity[i].text.replace("\n", " ").split()))
                        project["Activity on this Job"] = activity
                    elif "Other open jobs by this client" in content.text:
                        other_open_jobs_by_this_client = content.contents[1].contents[3].attrs.get("data-other-jobs")
                        project["Other open jobs by this client"] = other_open_jobs_by_this_client
                        #TODO
                    elif "Similar Jobs on Upwork" in content.text:
                        similar_job = content.contents[1].contents[3].attrs.get("data-similar-jobs")
                        project["Similar Jobs on Upwork"] = similar_job
                        #TODO

            #information about client
            client_table = job_soup.find_all("div", class_="col-md-3")
            for client_data in client_table:
                if "About the Client" in client_data.text:
                    size = len(client_data)
                    client_info = []
                    for i in range(7,size):
                        if client_data.contents[i] != "\n":
                            client_info.append(" ".join(client_data.contents[i].text.replace("\n", " ").split()))
            project["About the client"] = client_info
        else:
            project = {
                "Job id": job_id,
                "Job link": job_link,
                "Job name": "Access is restricted to Upwork users only. Create an Account or Sign in to view this job post"
            }
        #write data to json file
        with open(JSON_PATH + job_id + ".json", "w", encoding='utf-8') as file:
            json.dump(project, file, indent=2, ensure_ascii=False)

def parser_runner(direction):
    # create dir where will be save json file
    if not os.path.exists(JSON_PATH):
        os.mkdir(JSON_PATH)
    #direction = "Python Machine Learning"
    number_of_page = 1
    mask_str = "&q=" + direction.replace(" ", "%20")
    path = MASK_URL + str(number_of_page) + mask_str
    pages = get_jobs_count(get_html(path))
    print("Jobs found for direction: " + '"' + direction + '"' + ": " + str(pages))

    #Find count of page
    if pages % 10 != 0:
        pages //= 10
        pages += 1
    else:
        pages //= 10

    print("All pages:" + str(pages))

    for number_of_page in range(1, pages + 1):
        print("At now parse pages: " + str(number_of_page))
        parser_for_one_page(get_html(MASK_URL + str(number_of_page) + mask_str))

def main():
    parser_runner("Node JS")


if __name__ == "__main__":
    main()