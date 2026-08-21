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

def compare_series(bh_returns, strat_returns):
    return pd.DataFrame({
        "Buy_Hold": [annualized_returns(bh_returns), annualized_volatility(bh_returns),
                     sharpe_ratio(bh_returns), max_drawdown(bh_returns)],
        "Strategy": [annualized_returns(strat_returns), annualized_volatility(strat_returns),
                     sharpe_ratio(strat_returns), max_drawdown(strat_returns)],
    }, index=["Annual Return", "Volatility", "Sharpe", "Max Drawdown"])


def portfolio_backtest(prices):
    returns = prices.pct_change()

    # Signal for EVERY stock at once (short MA > long MA per column)
    short_ma = prices.rolling(50).mean()
    long_ma  = prices.rolling(200).mean()
    signals = (short_ma > long_ma).astype(int)   # 1/0 matrix, all stocks

    # Look-ahead fix + strategy returns for every stock
    strat_returns = signals.shift(1) * returns

    # Equal-weight portfolio = average across all stocks each day
    bh_portfolio    = returns.mean(axis=1)        # axis=1 = average across columns (stocks)
    strat_portfolio = strat_returns.mean(axis=1)

    return bh_portfolio, strat_portfolio
if __name__ == "__main__":
    prices=load_prices()
    prices=clean_prices(prices)

    bh_p, strat_p = portfolio_backtest(prices)
    print("\n===== FULL S&P 500 PORTFOLIO =====")
    print(compare_series(bh_p, strat_p))   