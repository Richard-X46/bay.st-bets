import yfinance as yf
import pandas as pd
from yfinance.screener import EquityQuery
import logging
pd.set_option('display.max_columns', None)


# configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s')

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


def get_stocks_by_exchange(exchange_name: str = None):
    query = EquityQuery("is-in", ["exchange"] + [exchange_name])
    results = yf.screen(query, size=250, sortField="intradaymarketcap", sortAsc=False)
    df = pd.DataFrame(results["quotes"])
    df.sort_values("marketCap", ascending=False, inplace=True)
    df = df[cols]
    return df


# ---/// Ticker price history \\\ ---

price_cols = [
    "date", # Date of the record
    "open", # Opening price
    "high", # maximum price of the day
    "low",  # minimum price of the day
    "close",# Closing price
    "volume",# Trading volume
    "dividends",# Dividends paid
    "stock_splits",# stock splits
    "ticker", # Ticker symbol
]

def get_ticker_price_history(ticker: str):

    yf_ticker = yf.Ticker(ticker)
    data = yf_ticker.history(period="max", interval="1d", auto_adjust=True)
    data.reset_index(inplace=True)
    data["Ticker"] = ticker 
    # converting column names to match db model
    data.rename(columns={
        "Date": "date",
        "Open": "open",
        "High": "high",
        "Low": "low",
        "Close": "close",
        "Volume": "volume",
        "Dividends": "dividends",
        "Stock Splits": "stock_splits",
        "Ticker": "ticker"
    }, inplace=True)
    data = data[price_cols] # assert only required columns
   
    return data



# ---/// mutual funds indexes \\\ ---


# FundQuery("eq", ["exchange", "TOR"])

# yf.Ticker("0P00015LZD.TO").info


# dir(yf.Ticker("RY.TO").get_funds_data())



# EquityQuery('eq', ['quoteType', 'MUTUALFUND'])  # Invalid field







# EquityQuery('and', [
#     EquityQuery('is-in', ['exchange', 'TOR', ]),
#     EquityQuery('lt', ["epsgrowth.lasttwelvemonths", 15])
# ])

# screen_result['quotes'] = yf.screen(
#     EquityQuery('and', [
#         EquityQuery('is-in', ['exchange', 'TOR', ]),
#         EquityQuery('lt', ["epsgrowth.lasttwelvemonths", 15])
#     ]),
#     size=100,
#     sortField="intradaymarketcap",
#     sortAsc=False
# )





# fq =      FundQuery('eq', ['exchange', 'NAS'])


# yf.screen(fq, )

# ff =FundQuery('AND', [
# FundQuery('IS-IN', ['performanceratingoverall', 4, 5]),

# FundQuery('EQ', ['exchange', 'NAS'])
# ])

# data = yf.screen(ff,  )
# pd.DataFrame(data['quotes'])



# # trying to get canadian mutual funds from equityquery



# url = "https://query1.finance.yahoo.com/v1/finance/screener/predefined/saved"
# params = {
#     "count": 100,  # more rows
#     "formatted": "true",
#     "scrIds": "TOP_MUTUAL_FUNDS_CA",
#     "sortField": "percentchange",
#     "sortType": "DESC",
#     "start": 100,  # page 1
#     "useRecordsResponse": "true",
#     "fields": "ticker,symbol,longName,shortName,regularMarketPrice,regularMarketChangePercent",
#     "lang": "en-CA",
#     "region": "CA"
# }
# headers = {"User-Agent": "Mozilla/5.0"} 

# resp = r.get(url, params=params, headers=headers).json()

# funds = resp["finance"]["result"][0]['records']

# df = pd.DataFrame(funds)
# df


# funds_df = pd.DataFrame(funds)
# funds_df

# funds_df.to_csv("/Users/richardpears/tmx-bay.st/data/canadian_mutual_funds.csv", index=False)



# fund_ticks = funds_df['ticker'].tolist()

# data = {}
# for i, t in enumerate(fund_ticks):
#     print(f"Fetching data for {i}: {t}")
#     fund_data = yf.Ticker(t).history(period="max", interval="1d", auto_adjust=True)
#     data[t] = fund_data 

# fund_price_history = pd.concat(data)
# fund_price_history.reset_index(inplace=True)
# fund_price_history.rename(columns={"level_0": "ticker"}, inplace=True)

# fund_price_history.to_csv("/Users/richardpears/tmx-bay.st/data/canadian_mutual_funds_price_history.csv", index=False)

# # size of df in mb



if __name__ == "__main__":



    # # # test get stocks by exchange
    # history_df = backfill_ticker_price_history(["RY.TO", "TD.TO"])
    # history_df.columns
    # res = get_ticker_price_history("RY.TO")
    # print(res.head(),res.info())



    pass