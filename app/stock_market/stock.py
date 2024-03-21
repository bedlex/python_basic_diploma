""" Module to handle https://site.financialmodelingprep.com/ API queries """
from typing import Dict, Type, List, Any
import requests

from datetime import datetime

from app.log import error_log


class Stock:
    def __init__(self, setting: Type) -> None:
        """
        Class method to initialise Class object

        Parameters:
            setting (Type): Setting object with API keys and URL.
        Returns:
            None:
        """

        self.__STOCK_KEY_API: str = setting.STOCK_KEY_API
        self.__STOCK_API_URL: str = setting.STOCK_API_URL

    def get_stock(self, symbol: str) -> Dict[str, str] | None:
        """
        Class method to get stock by symbol.

        Parameters:
            symbol (str): Symbol to search.

        Returns:
            Dict[str,str]: Dict object
            if request not respond or method get any error.
        Exception:
            Any exception during execution are logged,
            and method returns None

        """
        try:

            endpoint = f'profile/{symbol}'
            payload = {"apikey": self.__STOCK_KEY_API}

            response = requests.get(self.__STOCK_API_URL + endpoint, params=payload)

            if response.status_code == 200:
                data = response.json()

                return self.__get_stock_format(data)

            return None

        except Exception as error:
            error_log(f"{self.__module__}, {self.__class__.__name__}.get_stock {error}")

            return None

    def __get_stock_format(self, data: List[Dict[str, Any]]) -> Dict[str, str]:
        """
        Class method to format data from get_stock request

        Parameters:
            data (List[Dict[str,str]]): Data from get_stock request
        Returns:
            Dict[str, Any]: Formatted data to get_stock
            None: if request not respond or method get any error.
        Exception:
            Any exception during execution are logged,
            and method returns None
        """
        result = dict()

        if len(data) > 0:
            article = data[0]

            if isinstance(article, dict):
                company = (f"Company name: {article.get('companyName')}\n\n"
                           f"Symbol: {article.get('symbol')}\n\n"
                           f"Industry: {article.get('industry')}\n\n"
                           f"Description: {article.get('description')}\n\n"
                           f"CEO: {article.get('ceo')}\n\n"
                           f"Full time employees: {article.get('fullTimeEmployees')}\n\n"
                           f"Website: {article.get('website')}\n\n"
                           f"Image: {article.get('image')}\n\n"
                           f"Phone: {article.get('phone')}\n\n"
                           f"Address: {article.get('address')}\n"
                           f"City: {article.get('city')}, "
                           f"state: {article.get('state')}, "
                           f"zip: {article.get('zip')}\n\n"
                           f"Currency: {article.get('currency')}\n"
                           f"Price: {article.get('price')}\n"
                           f"Range: {article.get('range')}\n"
                           f"Changes: {article.get('changes')}\n"
                           f"Exchange: {article.get('exchange')}\n"
                           f"Exchange Short Name: {article.get('exchangeShortName:')}\n"
                           f"Market cap: {article.get('mktCap')}\n"
                           f"IPO date: {article.get('ipoDate')}\n"
                           )

                result["symbol"] = article.get('symbol')
                result['company'] = company

        return result

    def company_search(self, company_name: str, limit: int) -> Dict[str, str] | None:
        """
        Class method to search company by specified company name.

        Parameters:
            company_name (str): Specified company name.
            limit(int): Result limit
        Returns:
            Dict[str,str]: Company dictianories
            None: if request not respond or method get any error.
        Exception:
            Any exception during execution are logged,
            and method returns None
        """
        try:

            endpoint = "search-name"

            payload = {
                "query": company_name,
                "limit": limit,
                "apikey": self.__STOCK_KEY_API
            }

            response = requests.get(self.__STOCK_API_URL + endpoint, params=payload)

            if response.status_code == 200:
                data = response.json()

                return self.__company_search_format(data)

            return None

        except Exception as error:
            error_log(f"{self.__module__}, {self.__class__.__name__}.company_search {error}")

            return None

    def __company_search_format(self, data: List[Dict[str, Any]]) -> Dict[str, str]:
        """
        Class method to format company_search method format response

        Parameters:
            data(List[Dict]): request data from company_search method
        returns:
            Dict[str, str]: Formatted data
        """
        result = dict()

        if isinstance(data, list):

            for el in data:
                article = (f"Company name: {el.get('name')}\n"
                           f"Symbol: {el.get('symbol')}\n"
                           f"Currency: {el.get('currency')}\n"
                           f"Stock Exchange: {el.get('stockExchange')}\n"
                           f"Exchange Short Name: {el.get('exchangeShortName')}")
                result[el.get('symbol')] = article

        return result

    def price_change(self, symbol: str) -> str | None:
        """
        Class method to get information price change by specified symbol
        through Stock API.

        Parameters:
            symbol (str): Specified symbol to search
        Returns:
            str: Searched symbol information
            None: if request not respond or method get any error.
        Exception:
            Any exception during execution are logged,
            and method returns None
        """
        endpoint = f"stock-price-change/{symbol}"

        payload = {"apikey": self.__STOCK_KEY_API}

        try:
            response = requests.get(self.__STOCK_API_URL + endpoint, params=payload)

            if response.status_code == 200:
                data = response.json()

                return self.__price_change(symbol=symbol, data=data)

            return None

        except Exception as error:
            error_log(f"{self.__module__}, {self.__class__.__name__}.price_change {error}")

            return None

    def __price_change(self, symbol: str, data: List[Dict[str, Any]]) -> str | None:
        """
        Class method to format price_change method response.

        Parameters:
            symbol(str): Symbol to search in price_change method
            data(List[Dict[str,Any]]): price_change method response
        Returns:
            str: Formatted data
        """
        if len(data) > 0:
            article = data[0]
            result = (f"Company symbol: {symbol}\n\n"
                      f"Stock price change\n\n"
                      f"Maximum price: {article.get('max')}\n"
                      f"10 years: {article.get('10Y')}\n"
                      f"5 years: {article.get('5Y')}\n"
                      f"3 years: {article.get('3Y')}\n"
                      f"1 year: {article.get('1Y')}\n"
                      f"Year to date: {article.get('ytd')}\n"
                      f"6 month: {article.get('6M')}\n"
                      f"3 month: {article.get('3M')}\n"
                      f"1 month: {article.get('1M')}\n"
                      f"1 day: {article.get('1D')}")

            return result

        return None

    def bookmark(self, symbol: str) -> Dict[str, str] | None:
        """
        Class to get information by specified symbol through
        Stock API

        Parameters:
            symbol(str): Search item
        Returns:
            Dict[str,str]: Searched item
            None: if request not respond or method get any error.
        Exception:
            Any exception during execution are logged,
            and method returns None
        """
        endpoint = f"quote/{symbol}"

        payload = {"apikey": self.__STOCK_KEY_API}

        try:
            response = requests.get(self.__STOCK_API_URL + endpoint, params=payload)

            if response.status_code == 200:
                data = response.json()

                return self.__bookmark(symbol=symbol, data=data)

            return None

        except Exception as error:
            error_log(f"{self.__module__}, {self.__class__.__name__}.bookmark {error}")

            return None

    def __bookmark(self, symbol: str, data: list[dict[str, str]]) -> Dict[str, str] | None:
        """
        Class method to format bookmark method response.

        Parameters:
            symbol(str): Symbol to search.
            data(Dict[str,Any]): response to format
        Returns:
            Dict[str,str]: Formatted data
            None: if data not passed validation
        """

        result = dict()

        if len(data) > 0:
            article = data[0]

            if isinstance(article, dict):
                company = (f"Symbol: {article.get('symbol')}\n"
                           f"Name: {article.get('name')}\n"
                           f"Price: {article.get('price')}\n"
                           f"Previous close: {article.get('previousClose')}\n"
                           f"Change: {article.get('change')}\n"
                           f"Day low: {article.get('dayLow')}\n"
                           f"Day High: {article.get('dayHigh')}")

                result["symbol"] = symbol
                result["company"] = company

                return result

        return None

    def __quote(self, symbol: str) -> dict | None:
        """
          Class method internal helper method to fetch a quote for a given stock symbol.

          Args:
              symbol (str): The stock symbol.

          Returns:
              Dict | None: A dictionary containing the quote or None if an error occurred.
          """

        try:

            endpoint = f'quote/{symbol}'
            payload = {"apikey": self.__STOCK_KEY_API}

            response = requests.get(self.__STOCK_API_URL + endpoint, params=payload)

            if response.status_code == 200:
                data = response.json()

                return data

            return None

        except Exception as error:
            error_log(f"{self.__module__}, {self.__class__.__name__}.__quote {error}")

            return None

    def high(self, symbol: str) -> str:
        """
        Class method fetches and returns the day high price for a given stock symbol.

        Args:
            symbol (str): The stock symbol.

        Returns:
            str: The day high price or 'Information not found' if the data was not found.
        """
        result = self.__quote(symbol=symbol)

        if result is not None and len(result) > 0:

            if result[0].get('dayHigh'):
                return result[0].get('dayHigh')

        return 'information not found'

    def low(self, symbol: str) -> str:
        """
        Class method fetches and returns the day low price for a given stock symbol.

        Args:
            symbol (str): The stock symbol.

        Returns:
            str: The day low price or 'Information not found' if the data was not found.
        """
        result = self.__quote(symbol=symbol)

        if result is not None and len(result) > 0:

            if result[0].get('dayLow'):
                return result[0].get('dayLow')

        return 'Information not found'

    def __custom(self, symbol: str, from_date: str, to_date: str) -> List[Dict] | None:
        """
        Internal helper function to fetch historical data for a given stock symbol and date.

        Args:
            symbol (str): The stock symbol.
            from_date (str): The start date in 'YYYY-MM-DD' format.
            to_date (str): The end date in 'YYYY-MM-DD' format.

        Returns:
            List[Dict] | None: A list of dictionaries containing historical data or None if an error occurred.
        """

        endpoint = f'historical-chart/1hour/{symbol}'

        payload = {
            "from": from_date,
            "to": to_date,
            "apikey": self.__STOCK_KEY_API
        }

        try:
            response = requests.get(self.__STOCK_API_URL + endpoint, params=payload)

            if response.status_code == 200:
                return response.json()

        except Exception as error:
            error_log(f"{self.__module__}, {self.__class__.__name__}.get_history {error}")

        return None

    def __custom_adjust_data(self, data: list[dict[str]]) -> dict[dict[str]]:
        """
        Adjust the historical stock data by combining the high, low, open, and close prices for each date.

        Args:
            data (list[dict[str]]): The historical stock data with date, time, high, low, open, and close values.

        Returns:
            dict[dict[str]]: A dictionary containing the adjusted data with date as the key and a nested
            dictionary as the value.
                The nested dictionary has time as the key and the high, low, open, and close prices as the values.
        """
        result_dict = dict()

        for dict_res in data:
            date, time = dict_res.get("date").strip().split()
            if date not in result_dict:
                result_dict[date] = {time: {
                                                "high": dict_res.get('high'),
                                                "low": dict_res.get('low'),
                                                "open": dict_res.get('open'),
                                                "close": dict_res.get('close')
                                            }}
                continue
            result_dict[date][time] = {
                "high": dict_res.get('high'),
                "low": dict_res.get('low'),
                "open": dict_res.get('open'),
                "close": dict_res.get('close')
            }

        return result_dict

    def __custom_sort_data(self, data: dict[dict[str, str]]) -> list[tuple[dict[str, str], Any]]:
        """
           Class method to sort a nested dictionary of string keys and string values by their date and time.
           The input `data` is a dictionary with date strings as keys and dictionaries with time strings
           as keys and string values as values. This method sorts the inner dictionaries by time
           and the outer dictionary by date, returning a list of lists where each sublist contains
           the sorted data for a given date.

           Args:
               data (dict[str, dict[str, str]]): A nested dictionary.

           Returns:
               list[list[str]]: A list of lists where each sublist contains the sorted.
           """
        for date_dict in data.keys():
            data[date_dict] = sorted(data[date_dict].items(), key=lambda x: datetime.strptime(x[0], '%H:%M:%S'))

        data = sorted(data.items(), key=lambda x: datetime.strptime(x[0], "%Y-%m-%d"))

        return data

    def custom(self, symbol: str, from_date: str, to_date: str) -> list[tuple[dict[str, str], Any]] | None:
        """
        Fetches and formats historical data for a given stock symbol and date.

        Args:
            symbol (str): The stock symbol.
            from_date (str): The start date in 'YYYY-MM-DD' format.
            to_date (str): The end date in 'YYYY-MM-DD' format.

        Returns:
            str: A formatted string containing historical data or 'Information not found' if the data was not found.
        """

        result = self.__custom(symbol=symbol, from_date=from_date, to_date=to_date)

        if result is not None and len(result) > 0:
            adjusted_dict = self.__custom_adjust_data(result)
            sorted_data = self.__custom_sort_data(adjusted_dict)

            return sorted_data

        return None
