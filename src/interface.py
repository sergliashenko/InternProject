import os

from sklearn.ensemble import RandomForestClassifier

import uwHtmlParser
import encoder
import model


def predict_job_by_link(job_link:str)->bool:
    job = uwHtmlParser.parse_one_job(job_link)
    return predict_job(job)


def predict_job(job):
    feature, _ = encoder.encode_job(job, is_labeled=False)
    predictor = model.load_model(os.path.join("resources", "data", "model.pkl"))
    print(predictor.predict_proba(feature))
    y_pred = predictor.predict(feature).astype(bool)
    return y_pred[0]


def predict_direction(direction:str)->list:
    jobs = uwHtmlParser.parser_for_direction(direction, max_number_of_jobs=100)
    return [predict_job(job) for job in jobs]


if __name__ == '__main__':
    print(predict_direction("angular js"))
