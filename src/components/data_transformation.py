# This file will contain code for data transformation, 
# such as changing category features into numerical features and handling one-hot or label encodings.

import sys
import os
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer ## To a Transformer pipeline of standardsclaer and onehotencoder
from sklearn.impute import SimpleImputer   ## For handling Missing Values
from sklearn.pipeline import Pipeline   ## For creating pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler  ## For data encoding and standardization

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object

# A DataTransformationConfig class is created to provide input paths for the data transformation component,
# specifically defining the path for the preprocessor object pickle file.
@dataclass
class DataTransformationConfig:
    ## preprocessor object filepath will create in artifact folder with preprocessor.pkl file name
    preprocessor_obj_filepath = os.path.join('artifacts','preprocessor.pkl')

#A DataTransformation class is then created with an __init__ method to initialize the data_transformation_config
class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()
    

# get_data_transformer_object is defined to create all the necessary pickle files for converting categorical features to numerical,
# performing standard scaling, and other transformations.
    def get_data_transformer_object(self):
        '''
            This function is responsible for data transformation 
        '''

        try:
            numerical_features = ['writing_score','reading_score']
            categorical_features = [
                'gender',
                'race_ethnicity',
                'parental_level_of_education',
                'lunch',
                'test_preparation_course'
            ]

            num_pipeline = Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy='median')), ## For handling missing values with their median
                    ("scaler",StandardScaler())  ## For Standardization of the data
                ]
            )

            cat_pipeline = Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="most_frequent")), ## For handling missing values in categorial features with mode.
                    ("one_hot_encoder",OneHotEncoder()),
                    ("scaler",StandardScaler(with_mean=False))
                ]
            )

            logging.info(f"Categorial Columns: {categorical_features}")
            logging.info(f"Numerical Columns: {numerical_features}")

            preprocessor = ColumnTransformer(
                [
                    ("num_pipeline",num_pipeline,numerical_features),
                    ("cat_pipeline",cat_pipeline,categorical_features)
                ]
            )

            return preprocessor
        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_data_transformation(self,train_path,test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Read Train and Test data completed")
            logging.info("Obtaining Preprocessor object")

            preprocessor_obj = self.get_data_transformer_object()
            target_column_name = 'math_score'
            numerical_features = ['writing_score','reading_score']

            ## Independent and Dependent Features
            ## X_train,y_train,X_test,y_test
            input_feature_train_df = train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df = train_df[target_column_name]
            input_feature_test_df = test_df.drop(columns=target_column_name,axis=1)
            target_feature_test_df = test_df[target_column_name]

            logging.info(f"Applying preprocessing object on training dataframe and testing dataframe")

            ## Standardization
            input_feature_train_arr = preprocessor_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessor_obj.transform(input_feature_test_df)

            ## Concatinating the independent and dependent features into single arr
            train_arr = np.c_[input_feature_train_arr,np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr,np.array(target_feature_test_df)]

            logging.info("Saved preprocessing object...")

            save_object(
                file_path = self.data_transformation_config.preprocessor_obj_filepath,
                obj = preprocessor_obj
            )

            return (train_arr,test_arr,self.data_transformation_config.preprocessor_obj_filepath)

        except Exception as e:
            raise CustomException(e,sys)