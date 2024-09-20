import pandas as pd
import numpy as np
from tscv import GapWalkForward
from sklearn.model_selection import GridSearchCV
from sklearn.tree import DecisionTreeClassifier

class ModelBuilding:
    def features_targets(df):
        try:
            feature_columns = ["Price_EMA5", "Price_EMA7", "Price_EMA14", "Price_EMA30", "EMA7_EMA14", "EMA7_EMA30", "MACD_MACDS", "14_day_trend_direction", "30_day_trend_direction"]
            X = df[feature_columns]
            y = df["Target"]
            return X,y
        except Exception as e:
            raise e
        
    def cross_val():
        try:
            cv = GapWalkForward(n_splits=15, gap_size=0, test_size=5)
            return cv
        except Exception as e:
            raise e
        
    def grid_seach(X, y, cv):
        param_grid = {
                        "max_depth":np.arange(3,10),
                        "criterion":["gini", "entropy"],
                        "min_samples_split": range(10,500,20)
                    }
        try:
            grid_dt = GridSearchCV(DecisionTreeClassifier(), param_grid=param_grid, cv=cv).fit(X,y)
            return grid_dt
        except Exception as e:
            raise e
        
    def model(X,y):
        model = DecisionTreeClassifier(criterion="gini", max_depth=3, max_leaf_nodes=30, min_samples_split=5)
        try:
            model.fit(X,y)
            y_pred = model.predict(X)
            return y_pred
        except Exception as e:
            raise e
        
