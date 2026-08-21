import pandas as pd
import numpy as np
from returns import load_prices,clean_prices,compute_returns
from metrices import annualized_returns, annualized_volatility, sharpe_ratio, max_drawdown

def moving_average_signal(prices,short=50,long=200):
    short_ma=prices.rolling(window=short).mean()
    long_ma=prices.rolling(window=long).mean()

    signal=np.where(short_ma>long_ma,1,0)

    return pd.Series(signal, index=prices.index)

def backtest(prices):
    signal=moving_average_signal(prices)
    daily_return=prices.pct_change()

    strategy_return=signal.shift(1)*daily_return

    return daily_return,strategy_return

def compare(price):
    buy_hold, strategy = backtest(price)
    return pd.DataFrame({
        "Buy_Hold": [annualized_returns(buy_hold), annualized_volatility(buy_hold),
                     sharpe_ratio(buy_hold), max_drawdown(buy_hold)],
        "Strategy": [annualized_returns(strategy), annualized_volatility(strategy),
                     sharpe_ratio(strategy), max_drawdown(strategy)],
    }, index=["Annual Return", "Volatility", "Sharpe", "Max Drawdown"])

if __name__ == "__main__":
    prices=load_prices()
    prices=clean_prices(prices)

    for tickers in["AAPL", "INTC", "WBD"]:
        print("\n=== Strategy vs Buy & Hold === for: ",tickers)
        print(compare(prices[tickers]))