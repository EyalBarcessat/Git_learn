import os
import numpy as np
import pandas as pd
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from dotenv import load_dotenv

# טעינת המפתח בצורה מאובטחת
load_dotenv()
API_KEY = os.getenv("API_KEY")

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

#  הגדרת פרמטרים בצורה מסודרת
parameters = {
  'start': '1',
  #'limit': 100,      # כמות המטבעות שתרצה
  'convert': 'USD'
}

# ניהול ה-Session וה-Headers
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': API_KEY,
}

session = Session()
session.headers.update(headers)

def get_coin_info(coin_symbol):
    try:
        # ביצוע הבקשה ל-API
        response = session.get(url, params=parameters)
        data = response.json()

        df = pd.json_normalize(data['data'])
        
        # עיבוד הנתונים בצורה נוחה להצגה
        df.sort_values('minted_market_cap', ascending=False, inplace=True)
        df.rename(columns={'quote.USD.price': 'price', 'quote.USD.percent_change_30d': 'percent_change_30d'}, inplace=True)
        df['price'] = df['price'].round(2)
        df['percent_change_30d'] = df['percent_change_30d'].round(2)
        df = df[['name', 'symbol', 'minted_market_cap', 'price', 'percent_change_30d']]
        
        coin_info = df[df['symbol'] == coin_symbol.upper()]
        if not coin_info.empty:
            print(f"Coin: {coin_info['name'].values[0]}\nSymbol: {coin_info['symbol'].values[0]}\nMarket Cap: {coin_info['minted_market_cap'].values[0]}\nPrice: {coin_info['price'].values[0]}\n30d Change: {coin_info['percent_change_30d'].values[0]}%")
        else:
            print(f"לא נמצא מטבע עם הסימול {coin_symbol}")
            return None
            
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(f"יש בעיית תקשורת: {e}")
    except KeyError:
        print("שגיאה: לא הצלחתי למשוך את הנתונים. וודא שה-API KEY תקין והכתובת נכונה.")


def main():
    symbol = input("Enter the symbol of the cryptocurrency you want to search for: ").upper()
    get_coin_info(symbol)

if __name__ == "__main__":
    main()