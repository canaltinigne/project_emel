# -*- coding: utf-8 -*-
"""some helper functions for project 1."""
import csv
import numpy as np
from gradient import sigmoid

def load_csv_data(data_path, sub_sample=False):
    """Loads data and returns y (class labels), tX (features) and ids (event ids)"""
    y = np.genfromtxt(data_path, delimiter=",", skip_header=1, dtype=str, usecols=1)
    x = np.genfromtxt(data_path, delimiter=",", skip_header=1)
    ids = x[:, 0].astype(np.int)
    input_data = x[:, 2:]
    feature_names =  np.genfromtxt(data_path, max_rows=2, delimiter=',', names=True).dtype.names

    # convert class labels from strings to binary (-1,1)
    yb = np.ones(len(y))
    yb[np.where(y=='b')] = 0        # Change -1 to 0
    
    # sub-sample
    if sub_sample:
        yb = yb[::50]
        input_data = input_data[::50]
        ids = ids[::50]

    return yb, input_data, ids, np.asarray(feature_names[2:])


def predict_labels(weights, data, model='reg'):
    """Generates class predictions given weights, and a test data matrix"""
    y_pred = []
    
    if model == 'log':                                      # For Logistic regression prediction
        y_pred = sigmoid(np.dot(data, weights))
        y_pred[np.where(y_pred <= 0.5)] = 0
        y_pred[np.where(y_pred > 0.5)] = 1
    else:
        y_pred = np.dot(data, weights)
        y_pred[np.where(y_pred <= 0)] = -1
        y_pred[np.where(y_pred > 0)] = 1
    
    return y_pred


def create_csv_submission(ids, y_pred, name):
    """
    Creates an output file in csv format for submission to kaggle
    Arguments: ids (event ids associated with each prediction)
               y_pred (predicted class labels)
               name (string name of .csv output file to be created)
    """
    with open(name, 'w') as csvfile:
        fieldnames = ['Id', 'Prediction']
        writer = csv.DictWriter(csvfile, delimiter=",", fieldnames=fieldnames)
        writer.writeheader()
        for r1, r2 in zip(ids, y_pred):
            writer.writerow({'Id':int(r1),'Prediction':int(r2)})
