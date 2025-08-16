import yfinance as yf
from datetime import datetime
class DataIngestion:
    def data_ingestion(ticker: str, start: datetime, end: datetime):
        try:
            data = yf.download(
                tickers=str(ticker),
                start=start,
                end=end,
                progress=False,  # Suppress progress output
                multi_level_index=False
            )
            print(ticker)
            print(start)
            print(end)
            # Verify data was retrieved successfully
            if data.empty:
                raise ValueError(f"No data retrieved for ticker {ticker}")
            
            return data
        
        except Exception as e:
            raise RuntimeError(f"Data ingestion failed for {ticker}: {str(e)}")