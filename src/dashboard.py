import streamlit as st
import pandas as pd 
from returns import load_prices,clean_prices,compute_returns
from metrices import summary,annualized_returns,annualized_volatility,sharpe_ratio,max_drawdown
from backtest import backtest,portfolio_backtest,compare_series


st.title("📈 Quant Alpha & Market Analytics Dashboard")

st.write("S&P 500 · backtesting · Sharpe · drawdown")

#Laod once and cache it 
@st.cache_data
def get_data():
    prices=load_prices()
    prices=clean_prices(prices)
    returns=compute_returns(prices)
    summarise=summary(returns)
    return prices,returns,summarise

prices, returns, summarise =get_data()

#sidebar pick a particular stock 

tickers=st.sidebar.selectbox("Select a stock: ",prices.columns)

# kpi card for choosen stock 

r=returns[tickers]
col1,col2,col3,col4=st.columns(4)
col1.metric("Annual Returns : ",f"{annualized_returns(r): .1%}")
col2.metric("Annual Volatility : ",f"{annualized_volatility(r): .1%}")
col3.metric("Sharpe : ",f"{sharpe_ratio(r): .2f}")
col4.metric("Max Drawdown : ",f"{max_drawdown(r): .1%}")

# price chart 
st.subheader(f"{tickers} -- Price History")
st.line_chart(prices[tickers])

#backtest -- strategy vs Buy and hold 

st.subheader(f"{tickers} - Strategy Vs Buy_and_Hold")

buy_hold, strategy=backtest(prices[tickers])
equity=pd.DataFrame({
    "Buy & Hold : ":(1 +buy_hold).cumprod(),
    "Strategy : ": (1+strategy).cumprod(),
})
st.line_chart(equity)

returns=compute_returns(prices)
summarise=summary(returns)

st.subheader("Metrics Summary — all stocks")
st.dataframe(summarise)
# --- Full-market portfolio backtest ---
st.header("🌐 Full S&P 500 Portfolio — Strategy vs Buy & Hold")
st.write("Equal-weight portfolio of all stocks. This is where trend-following shines.")

bh_p, strat_p = portfolio_backtest(prices)

port_equity = pd.DataFrame({
    "Buy & Hold": (1 + bh_p).cumprod(),
    "Strategy":   (1 + strat_p).cumprod(),
})
st.line_chart(port_equity)

st.subheader("Portfolio Performance Comparison")
st.dataframe(compare_series(bh_p, strat_p))