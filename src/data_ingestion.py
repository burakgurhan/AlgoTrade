import pandas as pd
import yfinance as yf
import numpy as np
import os
from datetime import datetime
import time

class DataIngestion:
    def data_ingestion(ticker:str, start:datetime, end:datetime):
        try:
            data = yf.download(tickers=f"{ticker}.IS", 
                               start=start,
                               end=end,
                               multi_level_index=False)
            return data
        except Exception as e:
            raise e