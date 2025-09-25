import pandas as pd
import numpy as np
class DataTransformation:
    def preprocessing(df:pd.DataFrame, ticker:str) -> pd.DataFrame:    
        try:
            df["Return"] = df["Close"].diff()
            df["Return_pct"] = df["Close"].pct_change()
            df["Target"] = np.where(df["Return"]>0, 1, 0)
            return df
        except Exception as e:
            raise f"Error in data preprocessing of {ticker}: {e}"