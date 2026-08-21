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


if __name__ == "__main__":
    prices=load_prices()
    prices=clean_prices(prices)

    appl_price=prices["AAPL"]

    buy_hold,strategy=backtest(appl_price)
    buy_equity=(1+buy_hold).cumprod()
    st_equity=(1+strategy).cumprod()

    
    print("Buy & Hold  final value of $1:", buy_equity.iloc[-1])
    print("Strategy    final value of $1:", st_equity.iloc[-1])

    print("\n=== Strategy vs Buy & Hold ===")
    comparison = pd.DataFrame({
        "Buy_Hold": [
            annualized_returns(buy_hold),
            annualized_volatility(buy_hold),
            sharpe_ratio(buy_hold),
            max_drawdown(buy_hold),
        ],
        "Strategy": [
            annualized_returns(strategy),
            annualized_volatility(strategy),
            sharpe_ratio(strategy),
            max_drawdown(strategy),
        ],
    }, index=["Annual Return", "Volatility", "Sharpe", "Max Drawdown"])

    print(comparison)