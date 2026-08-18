import pandas as pd
import requests
from io import StringIO      # add near your other imports at the top

URL="https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

HEADERS ={"User-Agent": "Mozilla/5.0"}

def get_sp500_tickers():
    response=requests.get(URL, headers=HEADERS)
    response.raise_for_status()

    table = pd.read_html(StringIO(response.text))
    sp500_table=table[0]
    tickers=sp500_table["Symbol"].tolist()
    return tickers

if __name__ == "__main__":
    tickers=get_sp500_tickers()
    print(f"Got {len(tickers)} tickers")
    print(tickers[:10])