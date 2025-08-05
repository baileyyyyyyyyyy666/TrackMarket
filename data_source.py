import requests
import pandas as pd
from datetime import datetime

class DataSource:
    def __init__(self):
        self.crypto_symbols = ['BTC', 'ETH', 'ADA']
        self.crypto_url = "https://www.alphavantage.co/query"
        self.api_key = "1EETPNHVFZX5QQ9P"

    def get_crypto_prices(self):
        crypto_list = []
        for symbol in self.crypto_symbols:
            params = {
                'function': 'GLOBAL_QUOTE',
                'symbol': symbol,
                'apikey': self.api_key
            }
            try:
                response = requests.get(self.crypto_url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    quote = data.get("Global Quote", {})
                    if quote:
                        price = float(quote.get('05. price', 0))
                        change_str = quote.get('10. change percent', quote.get('09. change percent', "0%"))
                        change = float(change_str.replace('%', '')) if change_str else 0.0
                        crypto_list.append({
                            'name': symbol,
                            'price': price,
                            'change': change,
                            'time': datetime.now()
                        })
            except Exception as error:
                print(f"Error getting crypto data for {symbol}: {error}")
        return pd.DataFrame(crypto_list)

