from src import textProcessing
import spacy

nlp = spacy.load("en")

#count the similarity between two vacancies(input two lists of keywords and threshold)
def similarity_between_two_vacancies(firstVacancies_keywords, secondVacancies_keywords, threshold):
    total_size = len(firstVacancies_keywords) * len(secondVacancies_keywords)
    total_similarity = 0

    for first_keyword in firstVacancies_keywords:
        for second_keyword in secondVacancies_keywords:
            cur_similarity = nlp(first_keyword).similarity(nlp(second_keyword))
            #check if word2vec knows about keyword
            if cur_similarity == 0.0:
                print("Word2Vec don't know about " + first_keyword + " vs " + second_keyword)
                total_size -= 1    #In order not to spoil the evaluation
            else:
                print(first_keyword + " " + second_keyword + ":" + str(cur_similarity))
                total_similarity += cur_similarity
    if total_size != 0:
        avg_similarity = total_similarity/total_size
    else:
        print("False " + str(0.0))
        return False

    if(avg_similarity > threshold):
        print("True: " + str(avg_similarity))
        return True
    else:
        print("False " + str(avg_similarity))
        return False

#count the similarity between all combination of vacancies(input data of keywords and threshold)
def similarity_for_all_vacancies(keywords_data, threshold):
    for first_id, firstVacancies_keywords in keywords_data.items():
        for second_id, secondVacancies_keywords in keywords_data.items():
            if(first_id != second_id):
                print("Similarity " + first_id + " vs " + second_id + ":")
                similarity_between_two_vacancies(firstVacancies_keywords, secondVacancies_keywords, threshold)

def main():
    # get keywords
    keywords = textProcessing.get_top_keywords(5)
    threshold = 0.3  # need modify
    similarity_for_all_vacancies(keywords, threshold)

if __name__ == "__main__":
    main()