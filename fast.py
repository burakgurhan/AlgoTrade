import datetime
import ta as ta
from pipeline import *

def get_stock(ticker):
    # DOWNLOAD DATA
    start = "2024-01-01"
    end = datetime.datetime.now().strftime("%Y-%m-%d")
    #df = yf.download(ticker, start=start, end=end, multi_level_index=True)

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

#get_today_lists(stock_list)