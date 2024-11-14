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
from pipeline import *


stock_list = ['AGHOL', 'AKBNK', 'AKSA', 'AKSEN', 'ALARK', 'ARCLK', 'ASELS', 'BIMAS', 'BRSAN', 'BTCIM', 'CANTE', 'CCOLA', 
              'CIMSA', 'DOAS', 'DOHOL', 'DURDO', 'ECZYT', 'EGEEN', 'EGSER', 'EKGYO', 'ENJSA', 'ENKAI', 'EREGL', 'FONET', 
              'FROTO', 'GARAN', 'GUBRF', 'HALKB', 'ISDMR', 'ISGYO', 'ISMEN', 'KCHOL', 'KLGYO', 'KOZAA', 'KOZAL', 'LMKDC', 
              'MAVI', 'MGROS', 'MIATK', 'ODAS', 'OTKAR', 'PETKM', 'PGSUS', 'QUAGR', 'REEDR', 'SAHOL', 'SASA', 'SISE', 
              'SKBNK', 'SNICA', 'TABGD', 'TAVHL', 'TCELL', 'THYAO', 'TKFEN', 'TKNSA', 'TTKOM', 'TUKAS', 'TUPRS', 
              'ULKER', 'VAKBN', 'VESBE', 'VESTL', 'YATAS', 'YKBNK', 'YYLGD', 'ZOREN']

def get_stock(ticker):
    # DOWNLOAD DATA
    ticker = f"{ticker}"
    start = "2024-01-01"
    end = datetime.now().strftime("%Y-%m-%d")
    #df = yf.download(ticker, start=start, end=end)

    data_ingest = Pipeline.get_data(ticker, start, end)
    df_processed = Pipeline.preprocess(data_ingest)  # Avoid modifying original df
    df_engineered = Pipeline.feature_engineer(df_processed)
    X, y = Pipeline.split_features_labels(df_engineered)
    y_pred = Pipeline.make_prediction(X, y)
    df_engineered["Prediction"] = y_pred
    df_engineered = Pipeline.calculate_technical_indicators(df_engineered)

    return df_engineered

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