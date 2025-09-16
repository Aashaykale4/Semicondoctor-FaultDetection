import sys
import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.pipeline import Pipeline

from src.constants import *
from src.logger import logging
from src.exception import CustomException
from src.utils.main_utils import MainUtils
from dataclasses import dataclass

@dataclass
class DataTransformationConfig:
    artifact_dir=os.path.join(artifact_folder)
    transformed_train_file_path=os.path.join(artifact_dir,'train.npy')
    transformed_test_file_path=os.path.join(artifact_dir,'test.npy')
    transformed_object_file_path=os.path.join(artifact_dir,'preprocessor.pkl')

class DataTransformation:
    def __init__(self,feature_store_file_path):
        self.feature_store_file_path=feature_store_file_path
        self.data_transformation_config=DataTransformationConfig()
        self.utils=MainUtils()

    @staticmethod
    def  get_data(feature_store_file_path:str)->pd.DataFrame:
        try:
            data=pd.read_csv(feature_store_file_path)
            data.rename(columns={'Good/Bad':TARGET_COLUMN},inplace=True)
            return data
        except Exception as e:
            raise CustomException(e,sys)
    
    def get_data_transformer_object(self):
     try:
        imput_step = ('imputer', SimpleImputer(strategy='constant', fill_value=0))
        scale_step = ('scaler', RobustScaler())

        preprocessor = Pipeline(steps=[imput_step, scale_step])
        return preprocessor
     except Exception as e:
        raise CustomException(e, sys)


    def initiate_data_transformation(self):
     try:
        dataframe = self.get_data(self.feature_store_file_path)
        x = dataframe.drop(columns=[TARGET_COLUMN])
        y = dataframe[TARGET_COLUMN].replace(-1, 0).values  # Fix labels

        xtrain, xtest, ytrain, ytest = train_test_split(x, y, test_size=0.2, random_state=42)
        preprocessor = self.get_data_transformer_object()
        xtrain_scaled = preprocessor.fit_transform(xtrain)
        xtest_scaled = preprocessor.transform(xtest)

        preprocessor_path = self.data_transformation_config.transformed_object_file_path
        os.makedirs(os.path.dirname(preprocessor_path), exist_ok=True)
        self.utils.save_object(file_path=preprocessor_path, obj=preprocessor)

        train_arr = np.c_[xtrain_scaled, ytrain]
        test_arr = np.c_[xtest_scaled, ytest]

        return train_arr, test_arr, preprocessor_path

     except Exception as e:
        raise CustomException(e, sys)
