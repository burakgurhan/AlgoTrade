import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import datetime
import plotly.express as px
from pipeline import *
from datetime import datetime

import yfinance as yf
import ta as ta
from tscv import GapWalkForward


from sklearn.ensemble import RandomForestClassifier



stock_list = ["BTC", "XRP", "ETH", "SOL", "BNB", 
              "DOGE", "AVAX", "SHIB", "LINK", "BCH", 
               "USDT", "TRX", "ADA", "PYTH", "LTC", 
               "NEAR", "MATIC", "DOT", "FTM"]

def get_stock(ticker):
  
    # DOWNLOAD DATA
    crypto_ticker = f"{ticker}-USD"
    start_date = "2023-01-01"
    end_date = datetime.now()

    data = yf.download(tickers=crypto_ticker, 
                       start=start_date, 
                       end=end_date, 
                       multi_level_index=False)
    df = pd.DataFrame(data=data["Adj Close"].values, index=data.index)
    df.columns = ["Close"]
    
    # DATA PREPROCESSING
    df["Return"] = df["Close"].diff()
    df["Return_pct"] = df["Close"].pct_change()
    df["Target"] = np.where(df["Return"]>0,1,0)
    

    # FEATURE ENGINEERING
    df["EMA7"] = ta.trend.ema_indicator(df["Close"], window=7, fillna=False)
    df["EMA30"] = ta.trend.ema_indicator(df["Close"], window=30, fillna=False)
    df["EMA90"] = ta.trend.ema_indicator(df["Close"], window=90, fillna=False)
    df["EMA180"] = ta.trend.ema_indicator(df["Close"], window=180, fillna=False)

    df["P_EMA7"] = np.where(df["Close"]>df["EMA7"], 1,0)
    df["P_EMA30"] = np.where(df["Close"]>df["EMA30"], 1,0)
    df["P_EMA90"] = np.where(df["Close"]>df["EMA90"], 1,0)
    df["P_EMA180"] = np.where(df["Close"]>df["EMA180"], 1,0)
    df["EMA7_EMA90"] = np.where(df["EMA7"]>df["EMA90"], 1,0)
    df["EMA7_EMA180"] = np.where(df["EMA7"]>df["EMA180"], 1,0)

    df.dropna(inplace=True)

    # TRAIN-TEST SPLIT
    X = df[["P_EMA7", "P_EMA30", "P_EMA90", "P_EMA180", "EMA7_EMA90", "EMA7_EMA180"]]
    y = df["Target"]

    # CROSS-VALIDATION
    #cv = GapWalkForward(n_splits=20, gap_size=0, test_size=5)

    # MODEL
    model = RandomForestClassifier(n_estimators=200, max_depth=3, max_leaf_nodes=30, min_samples_split=5)
    model.fit(X,y)

    df["Prediction"] = model.predict(X)

    # POSTPROCESSING
    df["Buy"] = np.where((df["Prediction"]==1), 1, 0)
    df["Sell"] = np.where((df["Prediction"]==0), 1, 0)
    df["Buy_DT_ind"] = np.where((df["Buy"] > df["Buy"].shift(1)), 1, 0)
    df["Sell_DT_ind"] = np.where((df["Sell"] > df["Sell"].shift(1)), 1, 0)

    df["Value_DT"]=1000*(1+(np.where(df["Buy"]==1, 0.90*df["Return_pct"], 0)).cumsum())

    return df

def get_today_lists(stock_list):
    buy_today = {}
    sell_today = {}
    for stock in stock_list:
        df = get_stock(stock)

        if df["Buy_DT_ind"].iloc[-1]==1:
            buy_today.update({stock:df["Close"][-1]})
        elif df["Sell_DT_ind"].iloc[-1]==1:
            sell_today.update({stock:df["Close"][-1]})
        else:
            pass

    return buy_today, sell_today

get_today_lists(stock_list)