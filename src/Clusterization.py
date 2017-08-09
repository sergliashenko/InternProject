from src import textProcessing
from src import word2VecDistance
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler


def main():
    # get keywords
    keywords = textProcessing.get_top_keywords(5)
    threshold = 0.3  # need modify
    matrix = word2VecDistance.similarity_for_all_vacancies(keywords, threshold)

    # X = StandardScaler().fit_transform(matrix)
    for i in range(5, 30):
        #TODO: add loop min_samples
        print(i)
        print("eps" + str(float(i)/100))
        db = DBSCAN(metric="precomputed", eps=float(i)/100, min_samples=2)
        y_db = db.fit_predict(matrix)
        print(y_db)
        #TODO print clustered docs



if __name__ == "__main__":
    main()