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
        """Veriyi DataIngestion sınıfı üzerinden çeker."""
        try:
            df = self.data_ingestion.data_ingestion(ticker, start, end, kind=kind)
            return df
        except Exception as e:
            raise RuntimeError(f"Pipeline failed while getting data for {ticker}: {e}") from e

        
    def preprocess(self, df, ticker):
        try:
            df = DataTransformation.preprocessing(df, ticker)
            return df
        except Exception as e:
            raise e
        
    def feature_engineer(self, df):
        try: 
            df = FeatureEngineering.feature_engineering(df)
            return df
        except Exception as e:
            raise e
    
    def split_features_labels(self, df):
        try:
            X, y = ModelBuilding.features_targets(self, df)
            return X,y
        except Exception as e:
            raise e
        
    def make_prediction(X,y):
        try:
            y_pred = ModelBuilding.model(X,y)
            return y_pred
        except Exception as e:
            raise e
        
    def calculate_technical_indicators(self, df):
        try:
            df = Utils.technical_indicators(df)
            return df
        except Exception as e:
            raise e
        
    def evaluate(self, y, y_pred):
        try:
            acc = Utils.evaluate_model(y, y_pred)
            return acc
        except Exception as e:
            raise e