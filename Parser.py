#!/usr/bin/env python

import urllib.request
import json
from bs4 import BeautifulSoup
from pip._vendor.progress import counter
MASK_URL = "https://www.upwork.com/o/jobs/browse/"

def get_html(url):
   req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
   page = urllib.request.urlopen(req)
   return page.read()

def get_pages_count(html):
    soup = BeautifulSoup(html, "html.parser")
    number_pages = soup.find("ul", class_="pagination pagination-sm m-xs-top-bottom pull-right")
    return int(number_pages.find_all("a")[-2].text)

def parse(html):
   projects = []

   #pars web page
   soup = BeautifulSoup(html, "html.parser")
   table = soup.find("div", class_="col-sm-12 jobs-list")
   jobs_names = table.find_all("h2", class_="m-0")                                                           #all projects names
   job_description = table.find_all("div", class_="description break")                                       #full description of projects
   #job_skills = job_description.find_all("span", class_="js-skills skills m-sm-top m-md-bottom")             #required skills for project
   count_of_projects = len(jobs_names)

   #creating map
   for it in range(count_of_projects):
       projects.append({
           "Job name": jobs_names[it].text.split(),
           "Job description": job_description[it].text.split()
           # "Required skills": [skill.text.split() for skill in job_skills][1:]
       })

   #write data to json file
   with open("someName.json", "w") as file:
       json.dump(projects, file, indent=2, ensure_ascii=False)


def main():
    page_count = get_pages_count(get_html(MASK_URL))
    print("Find pages count: ", page_count)
    projects = []
    for page in range(1, page_count+1):
        projects.extend(parse(get_html(MASK_URL + "?page=" + str(page))))

    for project in projects:
        print(project)
   #parse(get_html(MASK_URL))



if __name__ == "__main__":
   main()
