#!/usr/bin/env python
#from src import uwApiParser
from src import textProcessing
    
  
def main():
    # list_with_data = uwApiParser.get_jobs("Python", "Machine Learning")
    # uwApiParser.make_json_file(list_with_data)
    result = textProcessing.get_top_keywords(5)
    for i in result:
        print(i)
 
if __name__ == "__main__":
    main()