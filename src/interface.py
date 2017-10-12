import uwHtmlParser
import encoder
from sklearn.externals import joblib
import os

from typing import List, Tuple

model = joblib.load(os.path.join(os.path.dirname(os.path.realpath(__file__)),os.path.join("resources", "model2.pkl")))


def predict_job(job, model):
    feature, _ = encoder.encode_job(job, is_labeled=False)
    y_pred = model.predict_proba(feature)[0, 1]
    return y_pred


def predict_job_by_link(job_link: str, model) -> bool:
    job = uwHtmlParser.parse_one_job(job_link)
    return predict_job(job, model)


def predict_job_direction(direction: str, model, max_number_of_jobs=10) -> List[Tuple[str, float]]:
    jobs = uwHtmlParser.parser_for_direction(direction, max_number_of_jobs=max_number_of_jobs)
    return sorted([(job["link"], predict_job(job["job"], model)) for job in jobs], key=lambda x: x[1], reverse=True)


if __name__ == '__main__':
    from sklearn.externals import joblib
    import os

    model = joblib.load(os.path.join("resources", "model.pkl"))
    print(predict_job_by_link("https://www.upwork.com/job/Front-end-dev-for-web-and-mobile-Angular-Ionic_~01ce5f9a119916440a/", model))
