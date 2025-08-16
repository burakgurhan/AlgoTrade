import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV
import requests
import seaborn as sns
import ftplib
import streamlit as st

start_date = "2025-01-01"
end_date = "2025-08-19"
ticker_list = ["AKSA", "ISDMR", "ISMEN", "VESBE", "FROTO", "TUPRS","EGEEN"]
ticker = st.selectbox(options=ticker_list, label="Please Select a Stock")
stock_name = f"{ticker}.IS"
df = yf.download(tickers=stock_name, start=start_date, end=end_date, multi_level_index=False)

st.dataframe(df)  # Display DataFrame only once

st.line_chart(df["Close"])  # Plot only the Close price column

df.rename(columns={"Adj Close":"Price"}, inplace=True)  # We will work on 'Price' column.
df["Return"] = df["Price"].diff() # Calculate daily changes in price
df["Return_pct"] = df["Price"].pct_change() # Calculate daily percentage changes.
df["Target_cls"] = np.where(df["Return"]>0,1,0) # Mark positive days as 1, negative days as 0.

import ta as ta
df["EMA10"] = ta.trend.ema_indicator(df["Price"], window=10, fillna=False)
df["EMA30"] = ta.trend.ema_indicator(df["Price"], window=26, fillna=False)
df["MACD"] = ta.trend.macd(df["Price"], window_fast=12, window_slow=26, fillna=False,)
df["MACDS"] = ta.trend.macd_signal(df["Price"], window_fast=12, window_slow=26, fillna=False)

df["P_EMA10"] = np.where(df["Price"]>df["EMA10"], 1,0)
df["EMA10_EMA30"] = np.where(df["EMA10"]>df["EMA30"], 1,0)
df["MACD_MACDS"] = np.where(df["MACD"]>df["MACDS"], 1,0)


df.dropna(inplace=True)

# we will use only the following columns to predict target close.
predictor_list = ["P_EMA10",    "EMA10_EMA30",  "MACD_MACDS"]

X = df[predictor_list]
y = df["Target_cls"]

clf = DecisionTreeClassifier(max_depth=3, min_samples_split=30).fit(X,y)

st.write("Accuracy score: ", accuracy_score(y, clf.predict(X)))


df["Predicted_Signal"] = clf.predict(X)

df["Buy_DT"] = np.where((df["Predicted_Signal"]==1), 1, 0)
df["Sell_DT"] = np.where((df["Predicted_Signal"]==0), 1, 0)
df["Buy_DT_ind"] = np.where((df["Buy_DT"] > df["Buy_DT"].shift(1)), 1, 0)
df["Sell_DT_ind"] = np.where((df["Sell_DT"] > df["Sell_DT"].shift(1)), 1, 0)

df["Date"]=df.index
df["Value_DT"]=1000*(1+(np.where(df["Buy_DT"]==1,
                                 0.95*df["Return_pct"], 0)).cumsum())

st.write(f"Dönem başında ₺1000 olan yatırım dönem sonunda ₺ {round(df['Value_DT'][-1],2)} olmuştur")
# Plot price with buy/sell signals
st.line_chart(
    df[["Price", "Buy_DT_ind", "Sell_DT_ind"]].dropna()
)

# Scatter plots for buy/sell signals
st.scatter_chart(
    x=df.loc[df["Buy_DT_ind"] == 1, "Date"].values,
    y=df.loc[df["Buy_DT_ind"] == 1, "Price"].values,
    label="Buy",
    color="green",
    size=100  # Adjust size as needed
)
st.scatter_chart(
    x=df.loc[df["Sell_DT_ind"] == 1, "Date"].values,
    y=df.loc[df["Sell_DT_ind"] == 1, "Price"].values,
    label="Sell",
    color="red",
    size=100  # Adjust size as needed
)

