import json
import os
import nltk
from nltk import word_tokenize, WordNetLemmatizer

#dir with .json files
directory_path = "D:\ParserUpWork\src"
files = os.listdir(directory_path)
#filter only .json type
json_files = filter(lambda x: x.endswith('.json'), files)

data = []
for file_name in json_files:
   with open(file_name, "r", encoding="utf-8") as file:
       data.append(json.load(file))

#1 Tokenize
page_count = len(data)
tokens = ["0"] * page_count

for i in range(page_count):
    tokens[i] = word_tokenize(data[i]["Job name"])
    tokens[i] += word_tokenize(data[i]["Job description"])

#2 Lemmatize
lemmatizer = WordNetLemmatizer()
tokes = [lemmatizer.lemmatize(token) for token in tokens[0]]
print(tokes)




def main():
    # for i in tokens:
    #     print(i)
    # print(tokens[0])
    pass
if __name__ == "__main__":
    main()