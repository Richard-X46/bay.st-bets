import yfinance as yf
import pandas as pd
from yfinance.screener import EquityQuery
from datetime import timedelta
import plotly.graph_objects as go


# List of major Canadian stock exchanges

canada_exchanges = [
    "CNQ",  # Canadian National Stock Exchange
    "NEO",  # NEO Exchange
    "TOR",  # Toronto Stock Exchange
    "VAN"   # TSX Venture Exchange
]




def get_max_history(ticker):
    """Get the maximum historical data for a given ticker."""
    data = yf.download(ticker, period="max")
    if data is None:
        raise ValueError(
            f"Failed to download data for ticker '{ticker}'. Check the ticker symbol or network connection."
        )
    return data

### ----------/// Single Ticker Analysis

ticker = "MTDR"

data = get_max_history(ticker)
data['MA50'] = data['Close'].rolling(window=50).mean()
data['MA200'] = data['Close'].rolling(window=200).mean()

# Reset index to make Date a column
data.reset_index(inplace=True)

# Flatten multi-level columns (drop the ticker level)
data.columns = data.columns.droplevel(1)

# Helper function to get date ranges
def get_date_range(data, period):
    end_date = data['Date'].max()
    if period == '1d':
        start_date = end_date - timedelta(days=1)
    elif period == '1w':
        start_date = end_date - timedelta(weeks=1)
    elif period == '1m':
        start_date = end_date - timedelta(days=30)
    elif period == '3m':
        start_date = end_date - timedelta(days=90)
    elif period == '6m':
        start_date = end_date - timedelta(days=182)
    elif period == '1y':
        start_date = end_date - timedelta(days=365)
    elif period == '3y':
        start_date = end_date - timedelta(days=3*365)
    elif period == '5y':
        start_date = end_date - timedelta(days=5*365)
    else:  # 'max'
        start_date = data['Date'].min()
    return start_date, end_date

# Create figure
fig = go.Figure()
fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], mode='lines', name='Close'))
fig.add_trace(go.Scatter(x=data['Date'], y=data['MA50'], mode='lines', name='MA50'))
fig.add_trace(go.Scatter(x=data['Date'], y=data['MA200'], mode='lines', name='MA200'))

fig.update_layout(
    title='RY.TO Price with MA50 and MA200',
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1, label='1d', step='day', stepmode='backward'),
                dict(count=7, label='1w', step='day', stepmode='backward'),
                dict(count=1, label='1m', step='month', stepmode='backward'),
                dict(count=3, label='3m', step='month', stepmode='backward'),
                dict(count=6, label='6m', step='month', stepmode='backward'),
                dict(count=1, label='1y', step='year', stepmode='backward'),
                dict(count=3, label='3y', step='year', stepmode='backward'),
                dict(count=5, label='5y', step='year', stepmode='backward'),
                dict(step='all', label='max')
            ])
        ),
        rangeslider=dict(visible=True),
        type="date"
    )
)

fig.show(renderer="browser")



# screener 
# getting canadaian stock ticks for collating info on all the stocks

dir(yf.Sector("energy"))

yf.Sector("basic-materials").top_companies




query = EquityQuery()


query = EquityQuery('eq', ['peer_group', 'China Fund Aggressive Allocation Fund'])
results = yf.screen(query, size=250, sortField='intradaymarketcap', sortAsc=False)

df = pd.DataFrame(results['quotes'])
df['exchange'].value_counts()


# Filter and reorder the DataFrame columns
def filter_and_reorder_dataframe(df, cols, exchanges):
    """
    Filter and reorder the DataFrame columns based on the provided columns and exchanges.

    Args:
        df (pd.DataFrame): The input DataFrame.
        cols (list): The list of columns to reorder.
        exchanges (list): The list of exchanges to filter.

    Returns:
        pd.DataFrame: The filtered and reordered DataFrame.
    """
    df = df[cols]
    query = EquityQuery('and', ['eq', 'region', 'CA'], ['eq', 'exchange', exchanges])
    return df

