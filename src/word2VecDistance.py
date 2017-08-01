import src.textProcessing
import spacy
import en_core_web_sm

#nlp = spacy.load("en")   #this piece of code not work on my PC
nlp = en_core_web_sm.load()

#count the similarity between two jobs(input two lists of keywords and threshold)
def similarity_between_two_jobs(firstJob_keywords, secondJob_keywords, threshold):
    total_size = len(firstJob_keywords) + len(secondJob_keywords)
    total_similarity = 0
    for first_keyword in firstJob_keywords:
        for second_keyword in secondJob_keywords:
            total_similarity += nlp(first_keyword).similarity(nlp(second_keyword))
    avg_similarity = total_similarity/total_size
    if(avg_similarity > threshold):
        print(avg_similarity)
        return True
    else:
        print(avg_similarity)
        return False


def main():
    # get keywords
    # keywords = textProcessing.get_top_keywords(5)
    # for jobs in keywords:
    #     print(jobs)
    #     print([val for val in keywords[jobs]])

    firstJob_keywords =  [u'vk', u'facebook', u'script', u'project', u'viber']
    secondJob_keywords = [u'media', u'social', u'instagram', u'b2c', u'twitter']
    threshold = 0.3 #need modify
    similarity_between_two_jobs(firstJob_keywords, secondJob_keywords, threshold)


if __name__ == "__main__":
    main()