import pandas as pd
from src.data_ingestion import DataIngestion
from src.data_preprocessing import DataTransformation
from src.feature_engineering import FeatureEngineering
from src.model_building import ModelBuilding
from src.model_evaluation import ModelEvaluation
from src.utils import Utils

class Pipeline:
    def get_data(ticker, start, end):
        try:
            df = DataIngestion.data_ingestion(ticker, start, end)
            if df is None:
                raise RuntimeError(f"No data returned for {ticker}")
            if not isinstance(df.index, pd.DatetimeIndex):
                raise ValueError("Data index must be DatetimeIndex")
            return df
        except Exception as e:
            raise RuntimeError(f"Failed to get data for {ticker}: {str(e)}")
        
    def preprocess(df):
        try:
            df = DataTransformation.preprocessing(df)
            return df
        except Exception as e:
            raise e
        
    def feature_engineer(df):
        try: 
            df = FeatureEngineering.feature_engineering(df)
            return df
        except Exception as e:
            raise e
    
    def split_features_labels(df):
        try:
            X, y = ModelBuilding.features_targets(df)
            return X,y
        except Exception as e:
            raise e
        
    def make_prediction(X,y):
        try:
            y_pred = ModelBuilding.model(X,y)
            return y_pred
        except Exception as e:
            raise e
        
    def calculate_technical_indicators(df):
        try:
            df = Utils.technical_indicators(df)
            return df
        except Exception as e:
            raise e
        
    def evaluate(y, y_pred):
        try:
            acc = Utils.evaluate_model(y, y_pred)
            return acc
        except Exception as e:
            raise e
    
    