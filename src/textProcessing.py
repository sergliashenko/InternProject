from __future__ import division
import json
import os
import math
from nltk import word_tokenize
from nltk.stem.porter import *
from nltk.corpus import stopwords
import copy

# dir with .json files
DIR_PATH = "/Users/skondrat/repo/ParserUpWork/data_raw"

def count_tf(term, full_text, count_terms_in_text):
 count_term = full_text.count(term)
 return count_term/count_terms_in_text

def count_doc_with_word(word, pages):
  counter = 0
  for list_of_word in pages:
      if word in list_of_word:
          counter +=1
  return counter

def find_json_file_in_dir(path):
  files = os.listdir(path)
  # filter only .json type
  jsons = filter(lambda x: x.endswith('.json'), files)
  return jsons

def get_text_from_files(json_files_pull):
  list_data = []
  data = {}
  for file_name in json_files_pull:
     del list_data[:]
     with open(DIR_PATH + "/" + file_name, "r") as file:
         list_data.append(json.load(file))
         data[file_name] = list_data[:]
  return data

def find_all_key_words(jobs_data):
  # 1.Tokenize
  jobs_count = len(jobs_data)
  keys_list = list(jobs_data.keys())
  tokens = ["0"] * jobs_count
  for i in range(jobs_count):
     tokens[i] = word_tokenize(jobs_data.get(keys_list[i])[0]["Job name"])
     tokens[i] += word_tokenize(jobs_data.get(keys_list[i])[0]["Job description"])

  # for v in jobs_data.values():
  #     tokens[i] = word_tokenize(v["Job name"])
  #     tokens[i] = word_tokenize(v["Job description"])
  # 2.Filtering
  # Delete stop words, words which length <= 2 and digits
  # Switch all words to lower case
  filter_tokens = ["0"] * jobs_count
  for i in range(jobs_count):
      filter_tokens[i] = [item.lower() for item in tokens[i] if item not in stopwords.words("english") and len(item) > 2
                          and not item.isdigit()]

  # 3.Stemming
  #After Stemming was corrupted some words. For example: machine->machin, everyone->everyon, etc.
  stemm = ["0"] * jobs_count
  stemmer = PorterStemmer()
  for i in range(jobs_count):
     stemm[i] = [stemmer.stem(token) for token in filter_tokens[i]]

  # 4.TF
  tf = ["0"] * jobs_count
  for i in range(jobs_count):
     count_terms_in_text = len(stemm[i])
     tf[i] = [count_tf(term, stemm[i], count_terms_in_text) for term in stemm[i]]

  # 5.IDF
  idf = ["0"] * jobs_count
  tmp_list = []
  doc_counter = 0
  for i in range(jobs_count):
      del tmp_list[:]
      for word in range(len(stemm[i])):
          if tf[i][word] > 0:
              doc_counter = count_doc_with_word(stemm[i][word], stemm)
              tmp_list.append(math.log(jobs_count/doc_counter))
      idf[i] = tmp_list[:]

  # 6.TF-IDF
  dict_for_page = {}
  tfidf = ["0"] * jobs_count
  for i in range(jobs_count):
      dict_for_page.clear()
      for j in range(len(stemm[i])):
          # Make dict with word and tf-idf
          dict_for_page[stemm[i][j]] = tf[i][j] * idf[i][j]
      tfidf[i] = dict_for_page.copy()

  # 7.Sorted key-words
  tfidf = [sorted(map_index.items(), key=lambda x: -x[1]) for map_index in tfidf]
  return tfidf

#N - number of key-word on the page
def get_top_keywords(N):
  # list with text from all .json files
  data = get_text_from_files(find_json_file_in_dir(DIR_PATH))
  tfidf = find_all_key_words(data)

  files_names = list(data.keys())
  size = len(data)
  #top_keywords = ["0"] * size
  top_keywords = []
  top_keywords_with_files_names = {}
  # Return TOP N key-words
  for page in range(size):
      page_size = len(tfidf[page])
      del top_keywords[:]
      if N <= page_size:
          top_keywords = [key[0] for key in tfidf[page][:N]]
          top_keywords_with_files_names[files_names[page]] = top_keywords[:]
      else:
          print("Value of N which you entered, greater than count of word in job number " + str(page) +
                "\nWill be displayed maximum words in this job description. \nMaximum = " + str(page_size))
          top_keywords = [key[0] for key in tfidf[page][:page_size]]
          top_keywords_with_files_names[files_names[page]] = top_keywords[:]
  return top_keywords_with_files_names