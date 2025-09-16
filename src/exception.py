import sys

def error_message_details(error_message,error_details:sys):
        # exc_info() returns tuple of exception type, exception value, and traceback object
        _,_,exc_tb=error_details.exc_info()
        # file where error occurred
        file_name=exc_tb.tb_frame.f_code.co_filename
        line_number=exc_tb.tb_lineno
        error_message= f"Error occured in script: [{file_name}] line number: [{line_number} ]"
        return error_message

class CustomException(Exception):
    def __init__(self,error_message,error_details:sys):
       super().__init__(error_message)

       self.error_message=error_message_details(
           error_message,error_details=error_details
       )
    def __str__(self):
        return self.error_message
       