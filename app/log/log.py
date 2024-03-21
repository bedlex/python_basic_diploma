""" Module to handle error log file """
from datetime import datetime


def error_log(error: str) -> None:
    """
    Function to write any errors to log file

    Parameters:
        error (str): String message to write into error.log file
    Returns:
         None:
    """
    print(error)
    with open(file="error.log", mode="a", encoding='utf-8') as file:
        file.write(f"{datetime.now()}:\t\t{error}\n")
