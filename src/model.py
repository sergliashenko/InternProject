from src import encoder

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.externals import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import binarize
import numpy as np
from sklearn.metrics import confusion_matrix
import os
import json

from typing import Tuple


def prepare_data(path: str) -> Tuple[np.ndarray, np.ndarray]:
    features = []
    labels = []

    for root, dirs, files in os.walk(path):
        for f in files:
            if f.endswith(".json"):
                print(f)
                with open(os.path.join(root, f)) as ff:
                    job_desc = json.load(ff)

                feature, label = encoder.encode_job(job_desc)

                features.append(feature[0])
                labels.append(label[0])

    return np.array(features), np.array(labels)


def cross_validate(features: np.ndarray, labels: np.ndarray, n_folds: int=10):

    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2)
    rf = RandomForestClassifier(n_jobs=-1, class_weight="balanced")
    parameters_grid = {"n_estimators": [100, 300, 500, 700],
                       "max_features": ['sqrt', 'log2']}

    cv_rf = GridSearchCV(estimator=rf, param_grid=parameters_grid, scoring="f1", cv=n_folds, verbose=1, n_jobs=-1)
    cv_rf.fit(X_train, y_train)

    print(cv_rf.cv_results_)
    print(cv_rf.best_score_)
    y_pred = cv_rf.best_estimator_.predict_proba(X_test)
    y_pred = y_pred[:,0]
    for i in range(30, 90, 5):
        print(i)
        y_temp_pred = np.where(y_pred>(float(i)/100), 0.0, 1.0)
        print(classification_report(y_test, y_temp_pred))
        conf_m = confusion_matrix(y_test, y_temp_pred)
        conf_m_norm = conf_m.astype('float') / conf_m.sum(axis=1)[:, np.newaxis]
        print(conf_m)
        print(conf_m_norm)


    return cv_rf.best_estimator_


def test(features: np.ndarray, labels: np.ndarray) -> None:
    rf = RandomForestClassifier(200)

    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.33)
    rf.fit(X_train, y_train)
    y_pred = rf.predict_proba(X_test)
    y_pred = y_pred[:,0]
    for i in range(50, 90, 5):
        print(i)
        y_temp_pred = np.where(y_pred>(float(i)/100), 1.0, 0.0)
        print(confusion_matrix(y_test, y_temp_pred))
    print("y_test: %i\ty_pred: %i" % (sum(y_test), sum(y_pred)))
    print(classification_report(y_test, y_pred))


def train(features: np.ndarray, labels: np.ndarray, model_params):
    rf = RandomForestClassifier(**model_params)
    rf.fit(features, labels)
    return rf


def save_model(model, path):
    joblib.dump(model, path)


def load_model(path):
    return joblib.load(path)


def balance_dataset(features, labels):
    pos_num = int(np.sum(labels))
    neg_num = labels.shape[0] - pos_num
    idxs = np.random.randint(neg_num, size=pos_num*2)
    features = np.concatenate([features[labels == 1.0], features[labels == 0.0][idxs]])
    labels = np.concatenate([labels[labels == 1.0], labels[labels == 0.0][idxs]])
    return features, labels

def evaluate_features(path):
    model = load_model(path)
    # print(np.sort(model.feature_importances_)[::-1])
    # print(np.argsort(model.feature_importances_)[::-1])
    hui = np.sort(model.feature_importances_)[::-1]
    pizda = np.argsort(model.feature_importances_)[::-1]
    with open("/Users/skondrat/features.txt", "r") as fp:
        result = fp.readlines()
        result = [r.strip() for r in result]
    for index in range(100):
        i = pizda[index]
        print(result[i], hui[index]*100)


np.set_printoptions(threshold=np.nan)
if __name__ == '__main__':
    # evaluate_features(os.path.join("resources", "data", "model1.pkl"))
    # exit()
    features, labels = prepare_data(os.path.join("resources", "data"))
    # exit()
    print(features.shape)
    features, labels = balance_dataset(features, labels)
    # test(features, labels)
    print(features.shape)
    model = cross_validate(features=features, labels=labels)
    save_model(model, os.path.join("resources", "model2.pkl"))

