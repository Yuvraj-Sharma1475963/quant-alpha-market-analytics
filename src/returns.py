import pandas as pd 

def load_prices(path="data/prices.csv"):


    #loading data 
    prices=pd.read_csv(path,index_col=0,parse_dates=True)
    return prices


def clean_prices(prices):
    #cleaning the column which does not have any price data
    prices=prices.dropna(axis=1,how="all") # how="all" means that drop the column only if all its value is nan

    prices=prices.ffill()

    return prices

def compute_returns(prices):
    returns=prices.pct_change()
    returns=returns.dropna(how="all")
    return returns

if __name__ == "__main__":
    prices=load_prices()
    prices=clean_prices(prices)
    returns=compute_returns(prices)

    print("Returns shape: ",returns.shape)
    print(returns.tail())
