import streamlit as st
import os
import pandas as pd
import numpy as np
from datetime import datetime
from src.data_ingestion import DataIngestion
import yfinance as yf
from pipeline import *
import plotly.express as px
from fast import get_today_lists

stock_list = ["BTC", "XRP", "ETH", "SOL", "BNB", "DOGE","AVAX", "SHIB", "LINK", "BCH", 
               "USDT", "TRX", "ADA", "PYTH", "LTC", "NEAR", "MATIC", "DOT", "FTM",
               "XLM", "SAND", "PEPE", "MANA", "TROY", "TIA", "POL", "BCH"]

class App:
   
    st.title("Crypto Trade App")

    if st.button("Günlükleri Getir", type="primary"):
        
        st.subheader(f"Bugün al")
        buy_today, sell_today = get_today_lists(stock_list=stock_list)
        df_buy_today = pd.DataFrame(buy_today.items(), columns=["Ticker", "Fiyat"])
        df_sell_today = pd.DataFrame(sell_today.items(), columns=["Ticker", "Fiyat"])
        st.write("Bugün al: ")
        st.dataframe(df_buy_today)
        st.write("Bugün sat: ")
        st.dataframe(df_sell_today)
    
            

    ticker = st.selectbox(label="Hisse senedi seçin", options=stock_list)

    start, end = st.slider("Tarih aralığı belirleyin",value=[datetime(2025, 1, 1), datetime.today()])

    st.subheader("Hissenin Son 5 günlük verileri")

    df:pd.DataFrame = DataIngestion.data_ingestion(ticker, start, end)
    df.reset_index(inplace=True)
    st.dataframe(data=df.tail())

    st.subheader(f"{ticker} Kapanış Fiyatları")
    st.line_chart(data=df, x="Date", y="Close")


    st.write("This is a data science project, is not a financial advice.\
              Financial invesment has huge risks. Please do not make investment based on Algotrade webapp.")

    if st.button("Tahminleri Getir", type="primary"):
        
        # Call pipeline functions here
        data_ingest = Pipeline.get_data(ticker, start, end)
        df_processed = Pipeline.preprocess(data_ingest)  # Avoid modifying original df
        df_engineered = Pipeline.feature_engineer(df_processed)
        X, y = Pipeline.split_features_labels(df_engineered)
        y_pred = Pipeline.make_prediction(X, y)
        df_engineered["Prediction"] = y_pred
        df_engineered = Pipeline.calculate_technical_indicators(df_engineered)
        
        # Display predictions (replace with your desired output)
        
        
        st.write(f"₺1000 yatırımın dönem sonundaki değeri: ₺{df_engineered['Value_DT'].tail(1).values.round(2)}")
        
        
        # Create the combined figure
        fig = px.line(data_frame=df_engineered, x="Date", y="Close", title="Buy-Sell Signals")

                    # Add scatter plots for buy and sell points
        fig.add_scatter(x=df_engineered.loc[df_engineered["Buy_DT_ind"]==1, "Date"].values, 
                        y=df_engineered.loc[df_engineered["Buy_DT_ind"]==1, "Close"].values, 
                        mode='markers', name='Al', marker=dict(color='green', size=7))

        fig.add_scatter(x=df_engineered.loc[df_engineered["Sell_DT_ind"]==1, "Date"].values, 
                        y=df_engineered.loc[df_engineered["Sell_DT_ind"]==1, "Close"].values, 
                        mode='markers', name='Sat', marker=dict(color='red', size=7))

                    # Customize the figure (optional)
        fig.update_layout(xaxis_title="Tarih", yaxis_title="Kapanış Fiyatı")
        st.plotly_chart(fig)