#  For custom exception handling.

import sys
from logger import logging

def error_message_detail(error,error_detail:sys):
    ## exe_info() from this we are getting all the information regarding the error in which file occurend and line 
    ## stored all this info inside exe_tb variable 
    _,_,exe_tb = error_detail.exc_info()

    ## getting filename in which the error occured
    file_name = exe_tb.tb_frame.f_code.co_filename
    error_message = "Error occured in python script name [{0}] line number [{1}] error message[{2}]".format(
        file_name,
        exe_tb.tb_lineno,
        str(error)
    )

    return error_message


class CustomException(Exception):
    def __init__(self,error_message,error_detail:sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message,error_detail=error_detail)

    def __str__(self):
        return self.error_message
    
