import pandas as pd
import numpy as np
import ta as ta
from sklearn.linear_model import LinearRegression

class FeatureEngineering:
    def feature_engineering(df:pd.DataFrame):
        def calculate_trend(data, window_size):
            trends = []
            for i in range(len(data) - window_size + 1):
                y = data[i:i + window_size]
                x = np.arange(window_size).reshape(-1, 1)
                model = LinearRegression().fit(x, y)
                slope = model.coef_[0]
                trends.append(slope)
            return trends
        try:
            df["EMA5"] = round(df["Close"].rolling(window=5).mean(),2)
            df["EMA20"] = round(df["Close"].rolling(window=20).mean(),2)
            df["EMA50"] = round(df["Close"].rolling(window=50).mean(),2)
            df["EMA100"] = round(df["Close"].rolling(window=100).mean(),2)
        except Exception as e:
            raise e
        
        try:
            df["Price_EMA5"] = np.where((df["Close"]>df["EMA5"]), 1, 0)
            df["Price_EMA20"] = np.where((df["Close"]>df["EMA20"]), 1, 0)
            df["Price_EMA50"] = np.where((df["Close"]>df["EMA50"]), 1, 0)
            df["Price_EMA100"] = np.where((df["Close"]>df["EMA100"]), 1, 0)
            df["EMA5_EMA20"] = np.where((df["EMA5"]>df["EMA20"]), 1, 0)
            df["EMA5_EMA50"] = np.where((df["EMA5"]>df["EMA50"]), 1, 0)
            df["EMA20_EMA100"] = np.where((df["EMA20"]>df["EMA100"]), 1, 0)
            

            # Calculate trends for 14-day and 30-day windows
            df['14_day_trend'] = np.nan
            df['30_day_trend'] = np.nan

            df.iloc[13:, df.columns.get_loc('14_day_trend')] = calculate_trend(df['Close'].values, 14)
            df.iloc[29:, df.columns.get_loc('30_day_trend')] = calculate_trend(df['Close'].values, 30)

            # Determine trend direction
            df['14_day_trend_direction'] = np.where(df['14_day_trend'] > 0, 1, 0)
            df['30_day_trend_direction'] = np.where(df['30_day_trend'] > 0, 1, 0)
            return df
        except Exception as e:
            raise e
        