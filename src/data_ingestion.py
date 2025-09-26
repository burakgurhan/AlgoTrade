import pandas as pd
import yfinance as yf
from datetime import datetime

class DataIngestion:
    def data_ingestion(ticker:str, start:datetime, end:datetime, kind="stock") -> pd.DataFrame:
        try:
            # Determine if the ticker is for crypto or stock based on its length
            ticker = ticker.upper()
            # Crypto ingestion
            if kind == "crypto":
                data = yf.download(
                    tickers=f"{ticker}-USD", 
                    start=start,
                    end=end,
                    multi_level_index=False
                   )
            # Stock ingestion
            else:
                data = yf.download(
                    tickers=f"{ticker}.IS",
                    start=start,
                    end=end,
                    multi_level_index=False
                )
            
            if data.empty:
                raise ValueError(f"No data returned for {ticker}")
            
            return data
        except Exception as e:
            raise Exception(f"Error while fetching data for {ticker}: {e}")
