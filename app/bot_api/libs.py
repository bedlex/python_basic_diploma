from datetime import datetime, timedelta
from typing import Tuple, Dict


def validate_dates(from_date: str, to_date: str, day_qty: int = 10) -> tuple[bool, bool] | tuple[str, str]:
    """
    Function to validate two date strings and check if to_date is greater than or equal to from_date.

    Args:
        from_date (str): The date string for the "From Date" in the format 'YYYY-MM-DD'.
        to_date (str): The date string for the "To Date" in the format 'YYYY-MM-DD'.
        day_qty (int): Maximal difference between days. Defaults 10 days.
    Returns:
        (tuple[str, str] | tuple[bool, bool]): from_date, to_date if validated, if not False, False
    """
    try:
        from_date = datetime.strptime(from_date, '%Y-%m-%d')
        to_date = datetime.strptime(to_date, '%Y-%m-%d')

        if from_date > to_date:
            raise ValueError

        elif (to_date - from_date) > timedelta(days=day_qty):
            to_date = from_date + timedelta(days=day_qty)

    except ValueError:
        return False, False
    from_date_string = from_date.strftime("%Y-%m-%d")
    to_date_string = to_date.strftime("%Y-%m-%d")

    return from_date_string, to_date_string


def custom_dict_to_string(data: Tuple[str, Dict[str, str]]) -> str:
    """
    Function to convert a tuple into a formatted string.

    Args:
        data (Tuple[str, [Dict[str, str]]): A tuple consisting of a time string and a dictionary
        which contains stock information with keys 'high', 'low', 'open', and 'close'.

    Returns:
        str: A formatted string containing the time and stock information.
    """

    result_string = (f"\tTIME: {data[0]}\n"
                     f"\thigh: ${data[1].get('high')}\n"
                     f"\tlow: ${data[1].get('low')}\n"
                     f"\topen: ${data[1].get('open')}\n"
                     f"\tclose: ${data[1].get('close')}\n\n")
    return result_string
