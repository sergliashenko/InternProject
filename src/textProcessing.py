from __future__ import division
import json
import os
import math
from nltk import word_tokenize
from nltk.stem.porter import *
from nltk.corpus import stopwords

# dir with .json files
DIR_PATH = "D:\ParserUpWork\data_raw"

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
     with open(DIR_PATH + "/" + file_name, "r") as file:
         data.append(json.load(file))
  return data

def find_all_key_words(pages):
  # 1.Tokenize
  page_count = len(pages)
  tokens = ["0"] * page_count
  for i in range(page_count):
     tokens[i] = word_tokenize(pages[i]["Job name"])
     tokens[i] += word_tokenize(pages[i]["Job description"])

  # 2.Filtering
  # Delete stop words, words which length <= 2 and digits
  # Switch all words to lower case
  filter_tokens = ["0"] * page_count
  for i in range(page_count):
      filter_tokens[i] = [item.lower() for item in tokens[i] if item not in stopwords.words("english") and len(item) > 2 and not item.isdigit()]

  # 3.Stemming
  #After Stemming was corrupted some words. For example: machine->machin, everyone->everyon, etc.
  stemm = ["0"] * page_count
  stemmer = PorterStemmer()
  for i in range(page_count):
     stemm[i] = [stemmer.stem(token) for token in filter_tokens[i]]

  # 4.TF
  tf = ["0"] * page_count
  for i in range(page_count):
     count_terms_in_text = len(stemm[i])
     tf[i] = [count_tf(term, stemm[i], count_terms_in_text) for term in stemm[i]]

  # 5.IDF
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

  # 6.TF-IDF
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

#N - number of key-word on the page
def get_top_keywords(N):
  # list with text from all .json files
  data = get_text_from_files(find_json_file_in_dir(DIR_PATH))
  tfidf = find_all_key_words(data)

  size = len(data)
  top_keywords = ["0"] * size
  # Return TOP N key-words
  for page in range(size):
      page_size = len(tfidf[page])
      if N <= page_size:
          top_keywords[page] = [key[0] for key in tfidf[page][:N]]
      else:
          print("Value of N which you entered, greater than count of word in page number " + str(page) +
                "\nWill be displayed maximum for this page. \nMaximum = " + str(page_size))
          top_keywords[page] = [key[0] for key in tfidf[page][:page_size]]
  return top_keywords