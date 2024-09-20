import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score


class ModelEvaluation:
    def accuracy(y, y_pred):
        try:
            acc = accuracy_score(y_true=y, y_pred=y_pred)
            return acc
        except Exception as e:
            raise e