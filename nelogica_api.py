import pandas as pd
import requests
from http import HTTPStatus


class NelogicaAPI:
    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.token = self.auth()
        self.base_url = 'https://api-mktdata.nelogica.com.br/v1/'
    
    def auth(self):
        """
        Authenticate user and returns a token.
        :return: str: Authentication Token.
        """

        url = self.base_url + 'auth'
        headers = {'accept': 'application/json'}
        json_data = {
            'login': self.login,
            'password': self.password
        }
        
        response = requests.post(url, headers=headers, json=json_data)
        token = response.json().get('access_token')
        
        print('Status Code:', response.status_code)
        print('Reason:', response.reason)
        
        return token

    def get_candles(self, exchange, symbol, **kwargs):
        """
        Returns a Pandas DataFrame with candle data given filter params.
        :param exchange: str: Selected symbol's exchange.
        :param symbol: str: Listed asset's code.
        :kwarg from: str: initial date 'YYYY-MM-DD'.
        :kwarg to: str: final date 'YYYY-MM-DD'.
        :kwarg qty: int: Quantity.
        :kwarg interval: str: Time frequency.
        :kwarg adjust: bool: Adjusted close price.
        :return: pd.DataFrame.
        """

        url = self.base_url + 'instrument/candles'
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }

        params = {
            'exchange': exchange,
            'symbol': symbol,
            **kwargs
        }
        
        response = requests.get(url, headers=headers, params=params)

        status_code = response.status_code

        print('Status Code:', status_code)
        print('Reason:', response.reason)
        
        if status_code == HTTPStatus.OK:
            df_candles = pd.json_normalize(response.json())
            df_candles.columns = ['datetime', 'trades', 'open', 'high', 'low', 'close', 'vol', 'qty']

            return df_candles
