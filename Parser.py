#!/usr/bin/env python
import urllib.request
import json
from bs4 import BeautifulSoup

MASK_URL = "https://www.upwork.com/o/jobs/browse/?page="

def get_html(url):
 req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
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
 #pars web page
 soup = BeautifulSoup(html, "html.parser")
 table = soup.find("div", class_="col-sm-12 jobs-list")
 jobs_caption = table.find_all("h2", class_="m-0")                                           #all projects names
 job_description = table.find_all("div", class_="description break")                         #full description of projects
 count_of_projects_name = len(jobs_caption)

 #push categories to dict
 for it in range(count_of_projects_name):
     job_id = jobs_caption[it].find("a").get("href").replace("/o/jobs/job/", "")
     project = {
         "Job name": jobs_caption[it].text,
         "Job description": job_description[it].text
     }
     #write data to json file
     with open(job_id[:-1] + ".json", "w", encoding='utf-8') as file:
         json.dump(project, file, indent=2, ensure_ascii=False)

def main():
  direction = "Python Machine Learning"
  number_of_page = 1
    
  pages = get_jobs_count(get_html(MASK_URL + str(number_of_page) + "&q=" + direction.replace(" ", "%20")))
  print("Jobs found for direction: " + '"' + direction + '"' + ": " + str(pages))

  #Find count of page
  pages = pages // 10
  if pages % 10 != 0:
      pages += 1

  print("All pages:" + str(pages))

  for number_of_page in range(1, pages + 1):
      print("At now parse pages: " + str(number_of_page))
      parser_for_one_page(get_html(MASK_URL + str(number_of_page) + "&q=" + direction.replace(" ", "%20")))

  # TODO: 5) do the same with Upwork API


if __name__ == "__main__":
 main()