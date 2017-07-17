#!/usr/bin/env python
from src import uwApiParser
    
  
def main():
    list_with_data = uwApiParser.get_jobs("Python", "Machine Learning")
    uwApiParser.make_json_file(list_with_data)
 
if __name__ == "__main__":
    main()