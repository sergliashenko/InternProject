import json
import os


#dir with .json files
directory_path = "D:\ParserUpWork"
files = os.listdir(directory_path)
#filter only .json type
json_files = filter(lambda x: x.endswith('.json'), files)


for file_name in json_files:
    with open(file_name, "r", encoding="utf-8") as file:
        data = json.load(file)
        print(data)


def main():
    pass

if __name__ == "__main__":
    main()