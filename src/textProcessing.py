from __future__ import division
import json
import os
import math
from nltk import word_tokenize
from nltk.stem.porter import *
from nltk.corpus import stopwords

# dir with .json files
DIR_PATH = "D:\ParserUpWork\src"

def count_tf(term, full_text, count_terms_in_text):
   count_term = full_text.count(term)
   return count_term/count_terms_in_text

def count_doc_with_word(word, pages):
    counter = 0
    for i in pages:
        if word in i:
            counter +=1
    return counter

def find_json_file_in_dir(path):
    files = os.listdir(path)
    # filter only .json type
    jsons = filter(lambda x: x.endswith('.json'), files)
    return jsons

def get_text_from_files(json_files_pull):
    data = []
    for file_name in json_files_pull:
       with open(file_name, "r") as file:
           data.append(json.load(file))
    return data

def find_all_key_words(pages):
    # 1.Tokenize
    page_count = len(pages) - 1   # without .json file which generate function uwApiParser.py
    tokens = ["0"] * page_count
    for i in range(page_count):
       tokens[i] = word_tokenize(pages[i]["Job name"])
       tokens[i] += word_tokenize(pages[i]["Job description"])

    # 2.Delete stop words
    for i in range(page_count):
       for item in tokens[i]:
           if item in stopwords.words("english"):
               tokens[i].remove(item)

    # 3.Switch all words to lower case
    for i in range(page_count):
       tokens[i] = [token.lower() for token in tokens[i]]

    # 4.Stemming
    #After Stemming was corrupted some words. For example: machine->machin, everyone->everyon, etc.
    stemm = ["0"] * page_count
    stemmer = PorterStemmer()
    for i in range(page_count):
       stemm[i] = [stemmer.stem(token) for token in tokens[i]]

    # 5.TF
    tf = ["0"] * page_count
    for i in range(page_count):
       count_terms_in_text = len(stemm[i])
       tf[i] = [count_tf(term, stemm[i], count_terms_in_text) for term in stemm[i]]

    # 6.IDF
    idf = ["0"] * page_count
    tmp_list = []
    doc_counter = 0
    for i in range(page_count):
        del tmp_list[:]
        for word in range(len(stemm[i])):
            if tf[i][word] > 0:
                doc_counter = count_doc_with_word(stemm[i][word], stemm)
                tmp_list.append(math.log(page_count/doc_counter))
        idf[i] = tmp_list[:]

    # 7.TF-IDF
    dict_for_page = {}
    tfidf = ["0"] * page_count
    for i in range(page_count):
        dict_for_page.clear()
        for j in range(len(stemm[i])):
            # Make dict with word and tf-idf
            dict_for_page[stemm[i][j]] = tf[i][j] * idf[i][j]
        tfidf[i] = dict_for_page.copy()

    # 7.Sorted key-words
    tfidf = [sorted(map_index.items(), key=lambda x: -x[1]) for map_index in tfidf]

    return tfidf

def get_top_keywords(N):
    # list with text from all .json files
    data = get_text_from_files(find_json_file_in_dir(DIR_PATH))
    tfidf = find_all_key_words(data)

    size = len(data)-1
    top_keywords = ["0"] * size
    # Return TOP N key-words
    for page in range(size):
        top_keywords[page] = [key[0] for key in tfidf[page][:N]]
    return top_keywords


def main():
   result = get_top_keywords(5)
   for i in result:
       print(i)

if __name__ == "__main__":
   main()