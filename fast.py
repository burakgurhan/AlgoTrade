import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import datetime
import plotly.express as px

import yfinance as yf
import ta as ta
from tscv import GapWalkForward


from sklearn.model_selection import GridSearchCV
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score


stock_list = ['AGHOL', 'AKBNK', 'AKSA', 'AKSEN', 'ALARK', 'ARCLK', 'ASELS', 'BIMAS', 'BRSAN', 'BTCIM', 'CANTE', 'CCOLA', 
              'CIMSA', 'DOAS', 'DOHOL', 'DURDO', 'ECZYT', 'EGEEN', 'EGSER', 'EKGYO', 'ENJSA', 'ENKAI', 'EREGL', 'FONET', 
              'FROTO', 'GARAN', 'GUBRF', 'HALKB', 'ISDMR', 'ISGYO', 'ISMEN', 'KCHOL', 'KLGYO', 'KOZAA', 'KOZAL', 'LMKDC', 
              'MAVI', 'MGROS', 'MIATK', 'ODAS', 'OTKAR', 'PETKM', 'PGSUS', 'QUAGR', 'REEDR', 'SAHOL', 'SASA', 'SISE', 
              'SKBNK', 'SNICA', 'TABGD', 'TAVHL', 'TCELL', 'THYAO', 'TKFEN', 'TKNSA', 'TTKOM', 'TUKAS', 'TUPRS', 
              'ULKER', 'VAKBN', 'VESBE', 'VESTL', 'YATAS', 'YKBNK', 'YYLGD', 'ZOREN']

def get_stock(ticker):
  # DOWNLOAD DATA
  ticker = f"{ticker}.IS"
  start_date= "2024-01-01"
  end_date= datetime.datetime.today().strftime("%Y-%m-%d")
  df = yf.download(ticker, start=start_date, end=end_date)

  # DATA PREPROCESSING
  df["Return"] = df["Close"].diff()
  df["Return_pct"] = df["Close"].pct_change()
  df["Target"] = np.where(df["Return"]>0,1,0)
  df.drop(["Open", "High", "Low", "Adj Close", "Volume"], axis=1, inplace=True)
  df["Close"] = round(df["Close"], 2)

  # FEATURE ENGINEERING
  df["EMA5"] = round(df["Close"].rolling(window=5).mean(),2)
  df["EMA7"] = round(df["Close"].rolling(window=7).mean(),2)
  df["EMA14"] = round(df["Close"].rolling(window=14).mean(),2)
  df["EMA30"] = round(df["Close"].rolling(window=30).mean(),2)
  df["MACD"] = ta.trend.macd(df["Close"], window_fast=12, window_slow=26, fillna=False,)
  df["MACDS"] = ta.trend.macd_signal(df["Close"], window_fast=12, window_slow=26, fillna=False)
  df["RSI"] = ta.momentum.rsi(df["Close"], fillna=False)

  df["Price_EMA5"] = np.where((df["Close"]>df["EMA5"]), 1, 0)
  df["Price_EMA7"] = np.where((df["Close"]>df["EMA7"]), 1, 0)
  df["Price_EMA14"] = np.where((df["Close"]>df["EMA14"]), 1, 0)
  df["EMA5_EMA7"] = np.where((df["EMA5"]>df["EMA7"]), 1, 0)
  df["EMA7_EMA14"] = np.where((df["EMA7"]>df["EMA14"]), 1, 0)
  df["EMA7_EMA30"] = np.where((df["EMA7"]>df["EMA30"]), 1, 0)
  df["MACD_MACDS"] = np.where(df["MACD"]>df["MACDS"], 1,0)

  # TRAIN-TEST SPLIT
  X = df[["Price_EMA5", "Price_EMA7", "Price_EMA14", "EMA5_EMA7", "EMA7_EMA30", "EMA7_EMA14", "MACD_MACDS"]]
  y = df["Target"]

  # CROSS-VALIDATION
  cv = GapWalkForward(n_splits=20, gap_size=0, test_size=5)

  # MODEL
  model = RandomForestClassifier(n_estimators=200, max_depth=3, max_leaf_nodes=30, min_samples_split=5).fit(X,y)

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