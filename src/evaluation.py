from sklearn import metrics

from typing import List, Tuple, Callable


def calc_metrics(test_data: List[Tuple[dict, bool]], decision_func: Callable[[dict], bool]) -> None:
    job_descriptions, labels = zip(*test_data)
    predictions = map(decision_func, job_descriptions)

    print("Accuracy: %f" % metrics.accuracy_score(labels, predictions))
    print("F1: %f" % metrics.f1_score(labels, predictions))
    print("Precision: %f" % metrics.precision_score(labels, predictions))
    print("Recall: %f" % metrics.recall_score(labels, predictions))
