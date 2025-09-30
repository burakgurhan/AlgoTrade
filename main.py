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
        self.start, self.end = self.utils.get_dates()


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
        st.write("This is a data science project, is not a financial advice.\
                    Financial invesment has huge risks. Please do not make investment based on AlgoTrade webapp.")
        
        stock_tab, crypto_tab = st.tabs(["Hisse Senetleri", "Kripto Paralar"])

        with stock_tab:
            if st.button("Günlükleri Getir", key="stock_button", type="primary"):
                buy_today, sell_today = self.get_today_lists(
                    list=self.stock_list, 
                    start=self.start, 
                    end=self.end, 
                    kind="stock"
                    )
                st.session_state.df_buy_today = pd.DataFrame(buy_today.items(), columns=["Ticker", "Fiyat"])
                st.session_state.df_sell_today = pd.DataFrame(sell_today.items(), columns=["Ticker", "Fiyat"])
                

                col1, col2 = st.columns(2, gap="small")
                with col1:
                    st.subheader("Bugün al")
                    st.dataframe(st.session_state.df_buy_today)

                with col2:
                    st.subheader("Bugün sat")
                    st.dataframe(st.session_state.df_sell_today)

            ticker_selection = st.selectbox(label="Hisse senedi seçin", options=self.stock_list)
            ticker = ticker_selection.upper()
            kind = "stock"

            st.subheader("Hissenin Son 5 günlük verileri")
            try:
                df, y_pred = self.pipeline.run(ticker, self.start, self.end, kind)
                st.dataframe(
                    data=df.iloc[:,:7].tail(), 
                    use_container_width=True, 
                    hide_index=False, 
                    )

                st.subheader(f"{ticker} Kapanış Fiyatları")
                st.line_chart(
                    data=df, 
                    x="Date", 
                    y="Close", 
                    x_label="Tarih", 
                    y_label="Kapanış Fiyatı"
                )
            
                if "Value_DT" in df.columns:
                    st.write(f"₺1000 yatırımın dönem sonundaki değeri: ₺{df['Value_DT'].tail(1).values.round(2)}")

                fig = px.line(data_frame=df, x="Date", y="Close", title="Buy-Sell Signals")
                if "Buy_DT_ind" in df.columns:
                    fig.add_scatter(
                        x=df.loc[df["Buy_DT_ind"]==1, "Date"].values, 
                        y=df.loc[df["Buy_DT_ind"]==1, "Close"].values, 
                        mode='markers', 
                        name='Al', 
                        marker=dict(color='green', size=7)
                    )
                if "Sell_DT_ind" in df.columns:
                    fig.add_scatter(
                        x=df.loc[df["Sell_DT_ind"]==1, "Date"].values, 
                        y=df.loc[df["Sell_DT_ind"]==1, "Close"].values, 
                        mode='markers', 
                        name='Sat', 
                        marker=dict(color='red', size=7)
                    )
                fig.update_layout(xaxis_title="Tarih", yaxis_title="Kapanış Fiyatı")
                st.plotly_chart(fig)

            except Exception as e:
                st.error(f"Error loading data for {ticker}: {str(e)}")
                st.stop()

        with crypto_tab:
            if st.button("Günlükleri Getir", key="crypto_button", type="primary"):
                buy_today, sell_today = self.get_today_lists(
                    list=self.crypto_list, 
                    start=self.start, 
                    end=self.end, 
                    kind="crypto"
                )
                st.session_state.df_buy_today = pd.DataFrame(buy_today.items(), columns=["Ticker", "Fiyat"])
                st.session_state.df_sell_today = pd.DataFrame(sell_today.items(), columns=["Ticker", "Fiyat"])
                

                col1, col2 = st.columns(2, gap="small")
                with col1:
                    st.subheader("Bugün al")
                    st.dataframe(st.session_state.df_buy_today)

                with col2:
                    st.subheader("Bugün sat")
                    st.dataframe(st.session_state.df_sell_today)

            ticker_selection = st.selectbox(label="Crypto seçin", options=self.crypto_list)
            ticker = ticker_selection.upper()
            kind = "crypto"

            st.subheader("Hissenin Son 5 günlük verileri")
            try:
                df, y_pred = self.pipeline.run(
                    ticker, 
                    self.start, 
                    self.end, 
                    kind
                )
                st.dataframe(
                    data=df.iloc[:,:7].tail(), 
                    use_container_width=True, 
                    hide_index=False, 
                    )

                st.subheader(f"{ticker} Kapanış Fiyatları")
                st.line_chart(data=df, x="Date", y="Close", x_label="Tarih", y_label="Kapanış Fiyatı")
            
                if "Value_DT" in df.columns:
                    st.write(f"₺1000 yatırımın dönem sonundaki değeri: ₺{df['Value_DT'].tail(1).values.round(2)}")

                fig = px.line(data_frame=df, x="Date", y="Close", title="Buy-Sell Signals")
                if "Buy_DT_ind" in df.columns:
                    fig.add_scatter(
                        x=df.loc[df["Buy_DT_ind"]==1, "Date"].values, 
                        y=df.loc[df["Buy_DT_ind"]==1, "Close"].values, 
                        mode='markers', 
                        name='Al', 
                        marker=dict(color='green', size=7)
                    )
                if "Sell_DT_ind" in df.columns:
                    fig.add_scatter(
                        x=df.loc[df["Sell_DT_ind"]==1, "Date"].values, 
                        y=df.loc[df["Sell_DT_ind"]==1, "Close"].values, 
                        mode='markers', 
                        name='Sat', 
                        marker=dict(color='red', size=7)
                    )
                fig.update_layout(xaxis_title="Tarih", yaxis_title="Kapanış Fiyatı")
                st.plotly_chart(fig)

            except Exception as e:
                st.error(f"Error loading data for {ticker}: {str(e)}")
                st.stop()


if __name__ == "__main__":
    app = App()
    app.main()