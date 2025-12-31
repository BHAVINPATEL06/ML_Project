#  For common functionalities used across the application,
#  like reading a dataset from a database or saving a model to the cloud.

import os
import sys
import pandas as pd
import numpy as np
import dill

from src.exception import CustomException
from sklearn.metrics import r2_score

def save_object(file_path,obj):
    try:
        ## Fetching filepath in dir_path 
        dir_path = os.path.dirname(file_path)
        ## creating 'artifacts' directory if already exist don't show error
        os.makedirs(dir_path,exist_ok=True)

        ## Dumping object file like 'preprocessor.pkl' inside the 'artifacts' folder
        with open(file_path,'wb')as file_obj:
            dill.dump(obj,file_obj)

    except Exception as e:
        raise CustomException(e,sys)
    
def evaluate_model(X_train,y_train,X_test,y_test,models):
    try:
        report = {}
        for i in range(len(list(models))):
            model = list(models.values())[i]
            model.fit(X_train,y_train)

            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)

            train_model_score = r2_score(y_train,y_train_pred)
            test_model_score = r2_score(y_test,y_test_pred)

            report[list(models.keys())[i]] = test_model_score
        return report
    
    except Exception as e:
        raise CustomException(e,sys)
