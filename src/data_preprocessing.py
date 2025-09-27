import pandas as pd
import numpy as np
class DataTransformation:
    @staticmethod
    def preprocessing(df:pd.DataFrame, ticker:str) -> pd.DataFrame:    
        try:
            if df is None or df.empty:
                raise ValueError(f"Input DataFrame for {ticker} is empty or None")

            df = df.dropna()
            # Remove other columns except 'Close'
            df = df["Close"].to_frame()

            df["Return"] = df["Close"].diff()
            df["Return_pct"] = df["Close"].pct_change()
            df["Target"] = np.where(df["Return"]>0, 1, 0)
            return df
        
        except Exception as e:
            raise RuntimeError(
                f"\nError while preprocessing data for ticker: {ticker}\n"
                f"Original error: {str(e)}\n"
            )