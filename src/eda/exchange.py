import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

from yfinance.screener import EquityQuery
pd.set_option('display.max_columns', None)



# List of exchanges to filter stocks from Canada and the US
exchange_list = [
    # Canadian Exchanges
    "CNQ",  # Canadian Securities Exchange (formerly Canadian National Stock Exchange)
    "NEO",  # NEO Exchange
    "TOR",  # Toronto Stock Exchange (TSX)
    "VAN",  # TSX Venture Exchange (TSXV)
    # US Exchanges
    "NMS",  # NASDAQ Stock Market
    "NYQ",  # New York Stock Exchange (NYSE)
    "ASE",  # NYSE American (formerly AMEX)
    "BTS",  # BATS Global Markets
    "CXI",  # Cboe Exchange
    "NGM",  # NASDAQ Global Market
    "NCM",  # NASDAQ Capital Market
    "PCX",  # NYSE Arca
    "PNK",  # OTC Pink Market (Over-the-Counter)
    ]


# get top 250 stocks by market cap from any of the exchanges in exchange_list
# columns considered


# ---/// Get stocks by exchange \\\ ---

cols = [
    "shortName",  # Company name
    "symbol",  # Unique ticker
    "marketCap",  # Market capitalization
    "exchange",  # Exchange code
    "fullExchangeName",  # Full exchange name
    "currency",  # Currency
    "exchangeTimezoneName",  # Timezone
    "regularMarketPrice",  # Current price (add for live data)
    "regularMarketVolume",  # Daily volume (add for liquidity)
    "fiftyTwoWeekHigh",  # 52-week high (add for trends)
    "fiftyTwoWeekLow",  # 52-week low (add for trends)
    "trailingPE",  # Trailing P/E ratio (add for valuation)
    "forwardPE",  # Forward P/E ratio (add for valuation)
    "dividendYield",  # Dividend yield (add for income)
    "averageAnalystRating",  # Analyst rating (add for sentiment)
    ]

def get_stocks_by_exchange(exchange_name:str = None):
    query = EquityQuery("is-in", ["exchange"] + [exchange_name] )
    results = yf.screen(query, size=250, sortField='intradaymarketcap', sortAsc=False)
    df = pd.DataFrame(results['quotes'])
    df.sort_values("marketCap", ascending=False, inplace=True)
    df = df[cols]
    return df


# df = get_stocks_by_exchange("TOR")
# df.to_clipboard(index=False)
# df = get_stocks_by_exchange("TOR")



# ---/// Ticker price history \\\ ---

def get_ticker_price_history(ticker: str):
    tik = yf.Ticker(ticker)
    history_df = tik.history(period="max", interval="1d", auto_adjust=False)
    history_df.reset_index(inplace=True)
    history_df['ticker'] = ticker
    history_df = history_df.rename(columns={
        'Open': 'open',
        'High': 'high',
        'Low': 'low',
        'Close': 'close',
        'Volume': 'volume',
        'Dividends': 'dividends',
        'Stock Splits': 'stock_splits',
        'Date': 'date'
    })
    history_df.reset_index( inplace=True)
    history_df = history_df[['date', 'open', 'high', 'low', 'close', 'volume', 'dividends', 'stock_splits', 'ticker']]
    return history_df


get_ticker_price_history("AC.TO")    



# plot close price history

def plot_close_price_history_with_moving_averages(df):
    plt.figure(figsize=(12,6))
    plt.plot(df['date'], df['close'], label='Close Price')
    plt.plot(df['date'], df['ma_50'], label='50-Day MA', linestyle='--')
    plt.plot(df['date'], df['ma_200'], label='200-Day MA', linestyle='--')
    plt.title(f"Close Price History for {df['ticker'].iloc[0]}")
    plt.xlabel("Date")
    plt.ylabel("Close Price")
    plt.legend()
    plt.grid()
    plt.show()


# add moving averages  for 50 and 200

def moving_average(df):
    for window in [50, 200]:
        df[f'ma_{window}'] = df['close'].rolling(window=window).mean()
        df[f'ma_{window}'] = df[f'ma_{window}'].fillna(method='bfill')
    return df





# relativce strength index

def compute_rsi(closing_prices: pd.Series, window=14):
    delta = closing_prices.diff()
    gain=delta.clip(lower=0)
    loss = abs(delta.clip(upper=0))
    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi




df = get_ticker_price_history("AC.TO")
df["rsi"] = compute_rsi(df["close"])

df = moving_average(df)

plot_close_price_history_with_moving_averages(df)












fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), sharex=True)

# Top: Close price and moving averages
ax1.plot(df["date"], df["close"], label="Close Price")
ax1.plot(df["date"], df["ma_50"], label="50-Day MA", linestyle="--")
ax1.plot(df["date"], df["ma_200"], label="200-Day MA", linestyle="--")
ax1.set_title(f"{df['ticker'].iloc[0]} Price & Moving Averages")
ax1.set_ylabel("Price")
ax1.legend()
ax1.grid()

# Bottom: RSI
ax2.plot(df["date"], df["rsi"], label="RSI", color="purple")
ax2.axhline(70, color="red", linestyle="--", label="Overbought (70)")
ax2.axhline(30, color="green", linestyle="--", label="Oversold (30)")
ax2.set_title("Relative Strength Index (RSI)")
ax2.set_ylabel("RSI")
ax2.set_xlabel("Date")
ax2.legend()
ax2.grid()

plt.tight_layout()
plt.show()

# ----/// Rough work


# df = get_stocks_by_exchange("NYQ")


# ticker_list = df['symbol'].tolist()

# yf.Tickers(ticker_list[:10]).download()


# dir(yf.Tickers(ticker_list[:10]))

# yf.Ticker("AMZN").info


# info = {}
# for x,i in enumerate(ticker_list):
#     print(i,x)
#     info[i] = yf.Ticker(i).info






# tech = yf.Sector("technology")
# software = yf.Industry("software-infrastructure")

# # Common information
# tech.key
# tech.name
# tech.symbol
# tech.ticker
# tech.overview
# tech.top_companies
# tech.research_reports

# # Sector information
# tech.top_etfs
# tech.top_mutual_funds
# tech.industries

# # Industry information
# software.sector_key
# software.sector_name
# software.top_performing_companies
# software.top_growth_companies
