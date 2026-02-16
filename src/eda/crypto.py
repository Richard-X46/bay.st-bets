import yfinance as yf

# btc usd history

def get_btc_usd_history(period: str = "max", interval: str = "1d"):
    btc = yf.Ticker("BTC-USD")
    data = btc.history(period=period, interval=interval)
    # flatten the multi-level columns if necessary

    return data


df = get_btc_usd_history()
print(df.head())
df

df.columns

# ...existing code...

def backtest_moving_average(df, short_window=20, long_window=50):
    df = df.copy()
    df['short_ma'] = df['Close'].rolling(window=short_window).mean()
    df['long_ma'] = df['Close'].rolling(window=long_window).mean()
    df['signal'] = 0
    df['signal'][short_window:] = (df['short_ma'][short_window:] > df['long_ma'][short_window:]).astype(int)
    df['positions'] = df['signal'].diff()
    # Calculate returns
    df['daily_return'] = df['Close'].pct_change()
    df['strategy_return'] = df['daily_return'] * df['signal'].shift(1)
    cumulative_return = (1 + df['strategy_return']).cumprod() - 1
    return df, cumulative_return

df = get_btc_usd_history()
backtest_df, cumulative_return = backtest_moving_average(df)
print("Cumulative strategy return:", cumulative_return.iloc[-1])
