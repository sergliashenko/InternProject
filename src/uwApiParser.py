from _csv import list_dialects

import upwork
import json

PUBLIC_KEY = "xxxxxxx"
SECRET_KEY = "xxxxxxxxxxxxxx"

#Function get_jobs outputs not real data from upwork site, output - hardcoded data
def get_jobs(query, title):
    #Initializing the client
    # client = upwork.Client(public_key, secret_key)
    # data = {'q': query, 'title': title}
    # job_info = client.provider_v2.search_jobs(data=data)
    # return job_info

    #This is example of real data from upwork
    EXAMPLE_RESPONSE = [
      {'budget': 750,
       'category2': 'Web & Mobile Development',
       'client': {'country': None,
                  'feedback': 0,
                  'jobs_posted': 1,
                  'past_hires': 0,
                  'payment_verification_status': None,
                  'reviews_count': 0},
       'date_created': '2014-06-30T23:50:17+0000',
       'duration': None,
       'id': '~aaa9992d99e35a386e',
       'job_status': 'Open',
       'job_type': 'Fixed',
       'skills': ['css',
                  'css3',
                  'database-design',
                  'database-programming',
                  'english',
                  'html',
                  'javascript',
                  'mysql',
                  'php',
                  'python'],
       'snippet': u"Need a custom website <...>",
       'subcategory2': 'Web Development',
       'title': 'Looking for highly skilled web developer',
       'url': 'http://...',
       'workload': '30+ hrs/week'},
       {
         # Another job
         # ...
       },
       # ...
     ]

    return EXAMPLE_RESPONSE

#Function get_freelancer outputs not real data from upwork site, output - hardcoded data
def get_freelancer(query, title):
    # Initializing the client
    # client = upwork.Client(public_key, secret_key)
    # data = {'q': query, 'title': title}
    # freelancer = client.provider_v2.search_providers(data=data, page_offset=0, page_size=20)
    # return freelancer

    # This is example of real data from upwork
    EXAMPLE_RESPONSE = [
     {'categories2': ['Legal',
                      'Web & Mobile Development',
                      'Admin Support'],
      'country': 'India',
      'description': 'I do ...',
      'feedback': '4.8424790960452',
      'id': '~aaaa9999d3f394624e',
      'last_activity': 'June 17, 2014',
      'member_since': 'July 21, 2011',
      'name': 'John Johnson',
      'portfolio_items_count': '1',
      'portrait_50': 'https://...',
      'profile_type': 'Independent',
      'rate': '22.22',
      'skills': ['python',
                  'django-framework',
                  'mongodb',
                  'jquery',
                  'html5',
                  'postgresql'],
     'test_passed_count': '3',
     'title': 'Web Developer'},
     {
       # Another freelancer
     },
     # ...
    ]

    return EXAMPLE_RESPONSE

#Generate ".JSON" file
def make_json_file(list_with_data):
    id = list_with_data[0]["id"]
    #write data to json file
    with open(str(id) + ".json", "w"    ) as file:
        json.dump(list_with_data, file, indent=2, ensure_ascii=False)