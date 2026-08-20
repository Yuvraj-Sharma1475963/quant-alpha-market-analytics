import pandas as pd
import requests
from io import StringIO      # add near your other imports at the top
import yfinance as yf

URL="https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

HEADERS ={"User-Agent": "Mozilla/5.0"}

def get_sp500_tickers():
    response=requests.get(URL, headers=HEADERS)
    response.raise_for_status()

    table = pd.read_html(StringIO(response.text))
    sp500_table=table[0]
    tickers=sp500_table["Symbol"].tolist()
    return tickers

def download_prices(tickers, start="2020-01-01",end="2025-01-01"):

    data=yf.download(
        tickers,
        start=start,
        end=end,
        auto_adjust=True
    )
    price=data["Close"]
    return price

if __name__ == "__main__":
    tickers=get_sp500_tickers()

    sample=tickers[:5]
    prices=download_prices(sample)

    print(prices.shape)
    print(prices.tail())