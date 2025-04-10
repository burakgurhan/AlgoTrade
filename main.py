import streamlit as st
import pandas as pd
from datetime import datetime
from src.data_ingestion import DataIngestion
from pipeline import *
import plotly.express as px
from fast import get_today_lists
from constants import stock_list, crypto_list

class App:
    def __init__(self):
        self.stock_list = stock_list
        self.crypto_list = crypto_list

    def format_ticker(self, tab, ticker):
        if tab == "stock":
            return ticker + ".IS"
        else:
            return ticker + "-USD"


    def main(self):
    
        st.title("Algorithmic Trade App")
        st.write("This is a data science project, is not a financial advice.\
                    Financial invesment has huge risks. Please do not make investment based on AlgoTrade webapp.")

        # Create Tabs
        tab1, tab2 = st.tabs(["BIST100", "CRYPTO"])

        with tab1:
            
            if st.button("Günlük Sinyalleri Getir", type="primary"):
                buy_today, sell_today = get_today_lists(stock_list=[self.format_ticker(tab="stock", ticker=ticker) for ticker in self.stock_list])
                df_buy_today = pd.DataFrame(buy_today.items(), columns=["Ticker", "Fiyat"])
                df_sell_today = pd.DataFrame(sell_today.items(), columns=["Ticker", "Fiyat"])
                st.markdown("### Bugün al: ")
                st.dataframe(df_buy_today)
                st.markdown("### Bugün sat: ")
                st.dataframe(df_sell_today)

            ticker_selection = st.selectbox(label="Hisse senedi seçin", options=stock_list)
            ticker = self.format_ticker(tab="stock", ticker=ticker_selection)
            start, end = st.slider("Tarih aralığı belirleyin",value=[datetime(2024, 1, 1), datetime.today()])

            st.subheader("Hissenin Son 5 günlük verileri")

            try:
                df: pd.DataFrame = Pipeline.get_data(ticker, start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d"))
                df.reset_index(inplace=True)
                #df.rename(columns={'index': 'Date'}, inplace=True)  # Standardize column name
                st.dataframe(data=df.tail())
            except Exception as e:
                st.error(f"Error loading data for {ticker}: {str(e)}")
                st.stop()

            st.subheader(f"{ticker} Kapanış Fiyatları")
            st.line_chart(data=df, x="Date", y="Close")


            st.write("This is a data science project, and this is not build for financial advice.\
                    Financial invesment has huge risks. Please do not make investment based on the output Algotrade webapp.")

            if st.button("Tahminleri Getir", type="primary"):
                try:
                    # Call pipeline functions with error handling
                    data_ingest = Pipeline.get_data(ticker, start, end)
                    df_processed = Pipeline.preprocess(data_ingest)  # Avoid modifying original df
                    df_engineered = Pipeline.feature_engineer(df_processed)
                    X, y = Pipeline.split_features_labels(df_engineered)
                    y_pred = Pipeline.make_prediction(X, y)
                    df_engineered["Prediction"] = y_pred
                    df_engineered = Pipeline.calculate_technical_indicators(df_engineered)
                    
                    # Display predictions (replace with your desired output)
                except Exception as e:
                    st.error(f"Error in trading pipeline: {str(e)}")
                    st.stop()
                
                
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

        with tab2:
            if st.button("Günlük Sinyalleri Getir", type="secondary"):
            
                st.subheader(f"Bugün al")
                buy_today, sell_today = get_today_lists(stock_list=[self.format_ticker(tab="crypto", ticker=ticker) for ticker in self.crypto_list])
                df_buy_today = pd.DataFrame(buy_today.items(), columns=["Ticker", "Fiyat"])
                df_sell_today = pd.DataFrame(sell_today.items(), columns=["Ticker", "Fiyat"])
                st.write("Bugün al: ")
                st.dataframe(df_buy_today, hide_index=True)
                st.write("Bugün sat: ")
                st.dataframe(df_sell_today, hide_index=True)
        
                

            ticker_selection_2 = st.selectbox(label="Hisse senedi seçin", options=self.crypto_list)
            ticker = self.format_ticker(tab2, ticker_selection_2)
            start, end = st.slider("Tarih aralığı belirleyin",value=[datetime(2024, 1, 1), datetime.today()])

            st.subheader("Hissenin Son 5 günlük verileri")

            try:
                df: pd.DataFrame = Pipeline.get_data(ticker, start, end)
                df.reset_index(inplace=True)
                df.rename(columns={'index': 'Date'}, inplace=True)  # Standardize column name
                st.dataframe(data=df.tail(), hide_index=True)
            except Exception as e:
                st.error(f"Error loading data for {ticker}: {str(e)}")
                st.stop()

            st.subheader(f"{ticker} Kapanış Fiyatları")
            st.line_chart(data=df, x="Date", y="Close")


            st.write("This is a data science project, is not a financial advice.\
                    Financial invesment has huge risks. Please do not make investment based on CryptoTrade webapp.")

            if st.button("Tahminleri Getir", type="secondary"):
            
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
                fig = px.line(data_frame=df_engineered[-120:], x="Date", y="Close", title="Buy-Sell Signals")

                # Add scatter plots for buy and sell points
                fig.add_scatter(x=df_engineered[-120:].loc[df_engineered["Buy_DT_ind"]==1, "Date"].values, 
                            y=df_engineered[-120:].loc[df_engineered["Buy_DT_ind"]==1, "Close"].values, 
                            mode='markers', name='Al', marker=dict(color='green', size=7))

                fig.add_scatter(x=df_engineered[-120:].loc[df_engineered["Sell_DT_ind"]==1, "Date"].values, 
                            y=df_engineered[-120:].loc[df_engineered["Sell_DT_ind"]==1, "Close"].values, 
                            mode='markers', name='Sat', marker=dict(color='red', size=7))

                # Customize the figure (optional)
                fig.update_layout(xaxis_title="Tarih", yaxis_title="Kapanış Fiyatı")
                st.plotly_chart(fig)

if __name__ == "__main__":
    app = App()
    app.main()