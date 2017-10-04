import uwHtmlParser
import encoder

from typing import List


def predict_job(job, model):
    feature, _ = encoder.encode_job(job, is_labeled=False)
    y_pred = model.predict(feature).astype(bool)
    return y_pred[0]


def predict_job_by_link(job_link: str, model) -> bool:
    job = uwHtmlParser.parse_one_job(job_link)
    return predict_job(job, model)


def predict_job_direction(direction: str, model, max_number_of_jobs=100) -> List[bool]:
    jobs = uwHtmlParser.parser_for_direction(direction, max_number_of_jobs=max_number_of_jobs)
    return [predict_job(job, model) for job in jobs]


if __name__ == '__main__':
    # print(predict_direction("angular js"))
    pass