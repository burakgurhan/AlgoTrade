from sklearn.metrics import accuracy_score, precision_score, recall_score
import pandas as pd
import numpy as np
from datetime import datetime
class Utils:
    def __init__(self) -> None:
        self.stock_list = ["AKSA", "ISMEN", "ISDMR", "FROTO", "TUPRS", "SAHOL", "EGEEN", "EGSER", "VESBE"]

    def get_dates(self) -> tuple[datetime, datetime]:
        end = datetime.now()
        end = datetime(end.year, end.month, end.day)
        start_year = end.year - 1
        start_month = end.month
        start_day = end.day
        start = datetime(start_year, start_month, start_day)
        return start, end

    def evaluate_model(y_true, y_pred):
        try:
            accuracy = accuracy_score(y_true, y_pred)
            
            return accuracy
        except Exception as e:
            raise e


    def technical_indicators(df:pd.DataFrame):
        try:
            df["Buy"] = np.where((df["Prediction"]==1), 1, 0)
            df["Sell"] = np.where((df["Prediction"]==0), 1, 0)
            df["Buy_DT_ind"] = np.where((df["Buy"] > df["Buy"].shift(1)), 1, 0)
            df["Sell_DT_ind"] = np.where((df["Sell"] > df["Sell"].shift(1)), 1, 0)
            df["Date"]=df.index
            df["Value_DT"]=1000*(1+(np.where(df["Buy"]==1, 0.90*df["Return_pct"], 0)).cumsum())
            return df
        except Exception as e:
            raise e