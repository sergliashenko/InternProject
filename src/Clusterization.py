from src import textProcessing
from src import word2VecDistance
from sklearn.cluster import DBSCAN

def clusterization():
    # get keywords
    keywords = textProcessing.get_top_keywords(5)
    threshold = 0.3  # need modify
    matrix = word2VecDistance.similarity_for_all_vacancies(keywords, threshold)
    groups = {}
    idx = 0

    for samp in range(1, 10):
        for e in range(5, 31):
            print("eps=" + str(float(e) / 100) + " min_samples=" + str(samp))
            db = DBSCAN(metric="precomputed", eps=float(e) / 100, min_samples=samp)
            y_db = db.fit_predict(matrix)
            groups.clear()
            idx = 0
            for k in keywords.keys():
                if y_db[idx] not in groups:
                    groups[y_db[idx]] = k
                else:
                    groups[y_db[idx]] += ";" + k
                idx += 1
            # print groups
            for g, file_name in groups.items():
                print("Group = " + str(g) + " Keywords: " + str(file_name))


def main():
    clusterization()

if __name__ == "__main__":
    main()