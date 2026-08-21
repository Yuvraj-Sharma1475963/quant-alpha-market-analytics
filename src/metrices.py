import pandas as pd
import numpy as np 
from returns import load_prices, clean_prices, compute_returns

TRADING_DAY=252 #  number of trading day in a year 

def annualized_returns(returns): # calculating anual returns
    return returns.mean()*TRADING_DAY;

def annualized_volatility(returns): # calculating annual volatility
    return returns.std()*np.sqrt(TRADING_DAY);

def sharpe_ratio(returns,risk_free=0.0): # calculating sharpe ratin 
    excces=annualized_returns(returns)-risk_free
    return excces/annualized_volatility(returns);

def max_drawdown(returns):
    # max drawdown is defined as the maximum downfall from highest point 
    equity=(1+returns).cumprod()

    peak=equity.cummax()

    drawdown=(equity-peak)/peak

    return drawdown.min()


def summary(returns):
    summary=pd.DataFrame({
        "annual_returns": annualized_returns(returns),
        "volatility":annualized_volatility(returns),
        "sharpe_ratio": sharpe_ratio(returns),
        "max_drawdown":max_drawdown(returns),
    })
    return summary

if __name__=="__main__":
    prices=load_prices()
    prices=clean_prices(prices)
    returns=compute_returns(prices)
    summary=summary(returns)

    print("=== Top 10 by Sharpe ===")
    print(summary.sort_values("sharpe_ratio", ascending=False).head(10))

    print("\n=== Bottom 10 by Sharpe ===")
    print(summary.sort_values("sharpe_ratio").head(10))

    # Save for the dashboard later
    summary.to_csv("data/metrics_summary.csv")
    print("\nSaved metrics for", len(summary), "stocks")