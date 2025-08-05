import requests
import pandas as pd
from datetime import datetime

class DataSource:
    def __init__(self):
        self.crypto_url = "https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=BTC,ETH,ADA&apikey=1EETPNHVFZX5QQ9P"
        self.weather_base_url = "https://api.open-meteo.com/v1/forecast"

    def get_crypto_prices(self):
        try:
            params = {
                'function': 'GLOBAL_QUOTE',
                'symbol': 'BTC,ETH,ADA',  # Update with your desired cryptocurrencies
            }
            response = requests.get(self.crypto_url, params=params)
            if response.status_code == 200:
                data = response.json()
                crypto_list = []
                for coin_name, coin_info in data.items():
                    crypto_list.append({
                        'name': coin_name,
                        'price': coin_info['05. price'],
                        'change': coin_info.get('09. change percent', 0),
                        'time': datetime.now()
                    })
                return pd.DataFrame(crypto_list)
        except Exception as error:
            print(f"Error getting crypto data: {error}")
            return pd.DataFrame()

    def get_weather(self):
        try:
            params = {
                'current_only': True,
                'hourly': False,
                'daily': False
            }
            response = requests.get(self.weather_base_url, params=params)
            if response.status_code == 200:
                weather_data = response.json()
                return {
                    'temperature': weather_data['current']['temperature'],
                    'humidity': weather_data['current']['humidity'],
                    'city': weather_data['location']['name'],
                    'time': datetime.now()
                }
        except Exception as error:
            print(f"Error getting weather data: {error}")
            return {}