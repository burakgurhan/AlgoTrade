import streamlit as st
import pandas as pd
from datetime import datetime, date
from src.data_ingestion import DataIngestion
from pipeline import Pipeline
import plotly.express as px
from fast import get_today_lists
from yaml import safe_load

# Load configuration from config.yaml
with open("config.yaml", "r") as file:
    config = safe_load(file)


# Choose your stock list: crypto or stocks
stock_list = config['stock_list']
crypto_list = config['crypto_list']

st.title("Algoritmik Trade App")

if st.button("Günlükleri Getir", type="primary"):
    st.subheader("Bugün al")
    buy_today, sell_today = get_today_lists(stock_list=stock_list)
    df_buy_today = pd.DataFrame(buy_today.items(), columns=["Ticker", "Fiyat"])
    df_sell_today = pd.DataFrame(sell_today.items(), columns=["Ticker", "Fiyat"])
    st.write("Bugün al: ")
    st.dataframe(df_buy_today)
    st.write("Bugün sat: ")
    st.dataframe(df_sell_today)

# Determine the dates for data ingestion in 365 days range
start, end = DataIngestion().get_dates()

ticker = st.selectbox(label="Hisse senedi seçin", options=stock_list)

# Use st.date_input for date selection
col1, col2 = st.columns(2)
with col1:
    start = st.date_input("Başlangıç tarihi", value=date(2024, 1, 1), max_value=date.today())
with col2:
    end = st.date_input("Bitiş tarihi", value=date.today(), min_value=start, max_value=date.today())

st.subheader("Hissenin Son 5 günlük verileri")
try:
    df = DataIngestion.data_ingestion(ticker, start, end)
    if df is not None and not df.empty:
        df = df.reset_index()
        st.dataframe(data=df.tail())
        st.subheader(f"{ticker} Kapanış Fiyatları")
        st.line_chart(data=df, x="Date", y="Close")
    else:
        st.warning("Veri bulunamadı.")
except Exception as e:
    st.error(f"Veri alınırken hata oluştu: {e}")

st.write("This is a data science project, and this is not built for financial advice. Financial investment has huge risks. Please do not make investment decisions based on the output of the Algotrade webapp.")

if st.button("Tahminleri Getir", type="primary"):
    try:
        data_ingest = Pipeline.get_data(ticker, start, end)
        df_processed = Pipeline.preprocess(data_ingest)
        df_engineered = Pipeline.feature_engineer(df_processed)
        X, y = Pipeline.split_features_labels(df_engineered)
        y_pred = Pipeline.make_prediction(X, y)
        df_engineered["Prediction"] = y_pred
        df_engineered = Pipeline.calculate_technical_indicators(df_engineered)

        if "Value_DT" in df_engineered.columns:
            st.write(f"₺1000 yatırımın dönem sonundaki değeri: ₺{df_engineered['Value_DT'].tail(1).values.round(2)}")

        fig = px.line(data_frame=df_engineered, x="Date", y="Close", title="Buy-Sell Signals")
        if "Buy_DT_ind" in df_engineered.columns:
            fig.add_scatter(x=df_engineered.loc[df_engineered["Buy_DT_ind"]==1, "Date"].values,
                            y=df_engineered.loc[df_engineered["Buy_DT_ind"]==1, "Close"].values,
                            mode='markers', name='Al', marker=dict(color='green', size=7))
        if "Sell_DT_ind" in df_engineered.columns:
            fig.add_scatter(x=df_engineered.loc[df_engineered["Sell_DT_ind"]==1, "Date"].values,
                            y=df_engineered.loc[df_engineered["Sell_DT_ind"]==1, "Close"].values,
                            mode='markers', name='Sat', marker=dict(color='red', size=7))
        fig.update_layout(xaxis_title="Tarih", yaxis_title="Kapanış Fiyatı")
        st.plotly_chart(fig)
    except Exception as e:
        st.error(f"Tahminler alınırken hata oluştu: {e}")