import sys
import os
import numpy as np
import pandas as pd
from zipfile import Path
from pymongo.mongo_client import MongoClient

from src.logger import logging
from src.constants import *
from src.exception import CustomException
from src.utils.main_utils import MainUtils
from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    artifact_folder:str=os.path.join(artifact_folder)

class DataIngestion:
    def __init__(self):
        self.data_ingestion_config=DataIngestionConfig()
        self.utils=MainUtils()
    
    def export_collection_as_dataframe(self,collection_name:str,db_name:str)->pd.DataFrame:
        try:
            mongo_client=MongoClient(MONGO_DB_URL)
            
            collection=mongo_client[db_name][collection_name]

            df=pd.DataFrame(list(collection.find()))


            if "_id" in df.columns.to_list():
                df=df.drop(columns=["_id"],axis=1)

            df.replace({'na':np.nan},inplace=True)
            return df
        except Exception as e:
            raise CustomException(e,sys)

    def export_data_into_feature_store_file_path(self):
     try:
        logging.info("Exporting data from mongodb ")
        raw_file_path=self.data_ingestion_config.artifact_folder
        os.makedirs(raw_file_path,exist_ok=True)
        sensor_data_df=self.export_collection_as_dataframe(collection_name=MONGO_COLLECTION_NAME,
                                                        db_name=MONGO_DATABASE_NAME)
        logging.info("saving exported data into feature store file path")
        
        feature_store_file_path=os.path.join(raw_file_path,"wafer_data.csv")
        sensor_data_df.to_csv(feature_store_file_path,index=False)

        return feature_store_file_path
     except Exception as e:
        raise CustomException(e,sys)
    
    def initiate_data_ingestion(self):
     logging.info("Entered initiated method of data_intigration class")
     try:
        feature_store_file_path=self.export_data_into_feature_store_file_path()
        logging.info("got data from mongodb ")
        logging.info(f"stored csv file in the following path {feature_store_file_path}")
        return feature_store_file_path
     except Exception as e:
        raise CustomException(e,sys)
        