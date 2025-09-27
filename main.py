import streamlit as st
import pandas as pd
from pipeline import Pipeline
import plotly.express as px
from src.utils import Utils
from src.constants import STOCK_LIST, CRYPTO_LIST

# Choose your stock list: crypto or stocks
stock_list = STOCK_LIST
crypto_list = CRYPTO_LIST

class App:
    st.title("Algoritmik Trade App")

    def __init__(self):
        self.stock_list = stock_list
        self.crypto_list = crypto_list
        self.pipeline = Pipeline()
        self.utils = Utils()

    def get_today_lists(self, list, start, end, kind):
        buy_today = {}
        sell_today = {}

        for ticker in list:
            df, y_pred = self.pipeline.run(ticker=ticker, start=start, end=end, kind=kind)

            if df["Buy_DT_ind"].iloc[-1]==1:
                buy_today.update({ticker:df["Close"][-1]})
            elif df["Sell_DT_ind"].iloc[-1]==1:
                sell_today.update({ticker:df["Close"][-1]})
            else:
                pass

        return buy_today, sell_today

    def main(self):
        st.title("Algoritmik Trade App")
        st.write("This is a data science project, is not a financial advice.\
                    Financial invesment has huge risks. Please do not make investment based on AlgoTrade webapp.")
        
        stock_tab, crypto_tab = st.tabs(["Hisse Senetleri", "Kripto Paralar"])

        start, end = Utils().get_dates()

        with stock_tab:
            if st.button("Günlükleri Getir", type="primary"):
                st.subheader("Bugün al")
                buy_today, sell_today = self.get_today_lists(list=self.stock_list, start=start, end=end, kind="stock")
                df_buy_today = pd.DataFrame(buy_today.items(), columns=["Ticker", "Fiyat"])
                df_sell_today = pd.DataFrame(sell_today.items(), columns=["Ticker", "Fiyat"])
                st.write("Bugün al: ")
                st.dataframe(df_buy_today)
                st.write("Bugün sat: ")
                st.dataframe(df_sell_today)

            ticker_selection = st.selectbox(label="Hisse senedi seçin", options=self.stock_list)
            ticker = ticker_selection.upper()
            #ticker = self.format_ticker(tab="stock", ticker=ticker_selection)
            kind = "stock"
            start, end = st.slider(min_value=start, max_value=end, label="Tarih aralığını seçin", value=(start, end), format="DD-MM-YYYY")

            st.subheader("Hissenin Son 5 günlük verileri")
            try:
                df, y_pred = self.pipeline.run(ticker, start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d"), kind)
                df.reset_index(inplace=True)
                #df.rename(columns={'index': 'Date'}, inplace=True)  # Standardize column name
                st.dataframe(
                    data=df.tail(), 
                    use_container_width=True, 
                    hide_index=True, 
                    )

                st.subheader(f"{ticker} Kapanış Fiyatları")
                st.line_chart(data=df, x="Date", y="Close", x_label="Tarih", y_label="Kapanış Fiyatı")
            
                if "Value_DT" in df.columns:
                    st.write(f"₺1000 yatırımın dönem sonundaki değeri: ₺{df['Value_DT'].tail(1).values.round(2)}")

                fig = px.line(data_frame=df, x="Date", y="Close", title="Buy-Sell Signals")
                if "Buy_DT_ind" in df.columns:
                    fig.add_scatter(x=df.loc[df["Buy_DT_ind"]==1, "Date"].values,
                                        y=df.loc[df["Buy_DT_ind"]==1, "Close"].values,
                                        mode='markers', name='Al', marker=dict(color='green', size=7))
                if "Sell_DT_ind" in df.columns:
                    fig.add_scatter(x=df.loc[df["Sell_DT_ind"]==1, "Date"].values,
                                        y=df.loc[df["Sell_DT_ind"]==1, "Close"].values,
                                        mode='markers', name='Sat', marker=dict(color='red', size=7))
                fig.update_layout(xaxis_title="Tarih", yaxis_title="Kapanış Fiyatı")
                st.plotly_chart(fig)

            except Exception as e:
                st.error(f"Error loading data for {ticker}: {str(e)}")
                st.stop()

        with crypto_tab:
            if st.button("Günlükleri Getir", type="primary"):
                st.subheader("Bugün al")
                buy_today, sell_today = self.get_today_lists(list=self.crypto_list, start=start, end=end, kind="crypto")
                df_buy_today = pd.DataFrame(buy_today.items(), columns=["Ticker", "Fiyat"])
                df_sell_today = pd.DataFrame(sell_today.items(), columns=["Ticker", "Fiyat"])
                st.write("##Bugün al: ")
                st.dataframe(df_buy_today)
                st.write("##Bugün sat: ")
                st.dataframe(df_sell_today)

            ticker_selection = st.selectbox(label="Crypto seçin", options=self.crypto_list)
            ticker = ticker_selection.upper()
            #ticker = self.format_ticker(tab="Crypto", ticker=ticker_selection)
            kind = "crypto"
            start, end = st.slider(min_value=start, max_value=end, label="Tarih aralığını seçin", value=(start, end), format="DD-MM-YYYY")

            st.subheader("Hissenin Son 5 günlük verileri")
            try:
                df, y_pred = self.pipeline.run(ticker, start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d"), kind)
                df.reset_index(inplace=True)
                #df.rename(columns={'index': 'Date'}, inplace=True)  # Standardize column name
                st.dataframe(
                    data=df.tail(), 
                    use_container_width=True, 
                    hide_index=True, 
                    )
                
                #df["Prediction"] = y_pred
                #df = self.pipeline.calculate_technical_indicators(df)

                st.subheader(f"{ticker} Kapanış Fiyatları")
                st.line_chart(data=df, x="Date", y="Close", x_label="Tarih", y_label="Kapanış Fiyatı")
            
                if "Value_DT" in df.columns:
                    st.write(f"₺1000 yatırımın dönem sonundaki değeri: ₺{df['Value_DT'].tail(1).values.round(2)}")

                fig = px.line(data_frame=df, x="Date", y="Close", title="Buy-Sell Signals")
                if "Buy_DT_ind" in df.columns:
                    fig.add_scatter(x=df.loc[df["Buy_DT_ind"]==1, "Date"].values,
                                        y=df.loc[df["Buy_DT_ind"]==1, "Close"].values,
                                        mode='markers', name='Al', marker=dict(color='green', size=7))
                if "Sell_DT_ind" in df.columns:
                    fig.add_scatter(x=df.loc[df["Sell_DT_ind"]==1, "Date"].values,
                                        y=df.loc[df["Sell_DT_ind"]==1, "Close"].values,
                                        mode='markers', name='Sat', marker=dict(color='red', size=7))
                fig.update_layout(xaxis_title="Tarih", yaxis_title="Kapanış Fiyatı")
                st.plotly_chart(fig)

            except Exception as e:
                st.error(f"Error loading data for {ticker}: {str(e)}")
                st.stop()


if __name__ == "__main__":
    app = App()
    app.main()

"""
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
start, end = Utils().get_dates()

ticker = st.selectbox(label="Hisse senedi seçin", options=stock_list)
kind = "stock" if ticker in stock_list else "crypto"
# Use st.date_input for date selection
start, end = st.slider(min_value=start, max_value=end, label="Tarih aralığını seçin", value=(start, end), format="DD-MM-YYYY")

st.subheader("Hissenin Son 5 günlük verileri")
try:
    df = DataIngestion.data_ingestion(ticker, start, end, kind=kind)
    if df is not None and not df.empty:
        df = df.reset_index()
        st.dataframe(data=df.tail(), hide_index=True, use_container_width=True)
        st.subheader(f"{ticker} Kapanış Fiyatları")
        st.line_chart(data=df, x="Date", y="Close", x_label="Tarih", y_label="Kapanış Fiyatı")
    else:
        st.warning("Veri bulunamadı.")
except Exception as e:
    st.error(f"Veri alınırken hata oluştu: {e}")

st.write("This is a data science project, and this is not built for financial advice. Financial investment has huge risks. Please do not make investment decisions based on the output of the Algotrade webapp.")

if st.button("Tahminleri Getir", type="primary"):
    try:
        pipeline = Pipeline()
        df, y_pred = pipeline.run(ticker, start, end, kind)
        df["Prediction"] = y_pred
        df = pipeline.calculate_technical_indicators(df)


        if "Value_DT" in df.columns:
            st.write(f"₺1000 yatırımın dönem sonundaki değeri: ₺{df['Value_DT'].tail(1).values.round(2)}")

        fig = px.line(data_frame=df, x="Date", y="Close", title="Buy-Sell Signals")
        if "Buy_DT_ind" in df.columns:
            fig.add_scatter(x=df.loc[df["Buy_DT_ind"]==1, "Date"].values,
                            y=df.loc[df["Buy_DT_ind"]==1, "Close"].values,
                            mode='markers', name='Al', marker=dict(color='green', size=7))
        if "Sell_DT_ind" in df.columns:
            fig.add_scatter(x=df.loc[df["Sell_DT_ind"]==1, "Date"].values,
                            y=df.loc[df["Sell_DT_ind"]==1, "Close"].values,
                            mode='markers', name='Sat', marker=dict(color='red', size=7))
        fig.update_layout(xaxis_title="Tarih", yaxis_title="Kapanış Fiyatı")
        st.plotly_chart(fig)
    except Exception as e:
        st.error(f"Tahminler alınırken hata oluştu: {e}")"""