from src.data_ingestion import DataIngestion
from src.data_preprocessing import DataTransformation
from src.feature_engineering import FeatureEngineering
from src.model_building import ModelBuilding
from src.model_evaluation import ModelEvaluation
from src.utils import Utils

class Pipeline:
    def __init__(self):
        self.data_ingestion = DataIngestion()
        self.data_transformation = DataTransformation()
        self.feature_engineering = FeatureEngineering()
        self.model_building = ModelBuilding()
        self.model_evaluation = ModelEvaluation()
        self.utils = Utils()


    def get_data(self, ticker, start, end, kind):
        try:
            df = self.data_ingestion.data_ingestion(ticker, start, end, kind)
            return df
        except Exception as e:
            raise RuntimeError(f"Pipeline failed while getting data for {ticker}: {e}") from e

        
    def preprocess(self, df, ticker):
        try:
            df = self.data_transformation.preprocessing(df, ticker)
            return df
        except Exception as e:
            raise e
        
    def feature_engineer(self, df):
        try: 
            df = self.feature_engineering.feature_engineering(df)
            return df
        except Exception as e:
            raise e
    
    def split_features_labels(self, df):
        try:
            X, y = self.model_building.features_targets(df)
            return X,y
        except Exception as e:
            raise e
        
    def make_prediction(self, X,y):
        try:
            y_pred = self.model_building.model(X,y)
            return y_pred
        except Exception as e:
            raise e
        
    def calculate_technical_indicators(self, df):
        try:
            df = self.utils.technical_indicators(df)
            return df
        except Exception as e:
            raise e
        
    def evaluate(self, y, y_pred):
        try:
            acc = self.utils.evaluate_model(y, y_pred)
            return acc
        except Exception as e:
            raise e

    def run(self, ticker, start, end, kind):
        df = self.get_data(ticker, start, end, kind)
        df = self.preprocess(df, ticker)
        df = self.feature_engineer(df)
        X, y = self.split_features_labels(df)
        y_pred = self.make_prediction(X, y)
        return df, y_pred