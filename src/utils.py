#  For common functionalities used across the application,
#  like reading a dataset from a database or saving a model to the cloud.

import os
import sys
import pandas as pd
import numpy as np
import dill

from src.exception import CustomException

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