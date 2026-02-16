# database models for tmx-bay.st
from sqlmodel import SQLModel, Field, Column,BigInteger
# from sqlalchemy import BigInteger
from datetime import datetime
from sqlalchemy import UniqueConstraint

# --- /// Exchange Indexes Table Model \\\ ---
"""
Exchange indexes for a given exchange from yf screener data.
"""
class ExchangeIndexes(SQLModel, table=True):
    __tablename__ = "exchange_indexes"
    id: int = Field(default=None, primary_key=True)
    shortName: str | None = Field(default=None, max_length=255)
    symbol: str = Field(index=True, max_length=20,unique=True)
    marketCap: int | None = Field(sa_column=Column(BigInteger()), default=None)
    exchange: str | None = Field(default=None, max_length=20)
    fullExchangeName: str | None = Field(default=None, max_length=100)
    currency: str | None = Field(default=None, max_length=20)
    exchangeTimezoneName: str | None = Field(default=None, max_length=50)
    regularMarketPrice: float | None = Field(default=None)
    regularMarketVolume: int | None = Field(default=None)
    fiftyTwoWeekHigh: float | None = Field(default=None)
    fiftyTwoWeekLow: float | None = Field(default=None)
    trailingPE: float | None = Field(default=None)
    forwardPE: float | None = Field(default=None)
    dividendYield: float | None = Field(default=None)
    averageAnalystRating: str | None = Field(default=None, max_length=100)
    last_updated: datetime = Field(default_factory=datetime.utcnow)

# ---/// Ticker History Table Model \\\ ---
"""
Historical price data for individual tickers.
"""

class EquityPriceHistory(SQLModel, table=True):
    __tablename__ = "equity_price_history"
    __table_args__ = (UniqueConstraint('ticker', 'date', name='uix_ticker_date'),)
    id: int = Field(default=None, primary_key=True)
    date: datetime
    open: float | None = Field(default=None)
    high: float | None = Field(default=None)
    low: float | None = Field(default=None)
    close: float | None = Field(default=None)
    volume: int | None = Field(default=None)
    dividends: float | None = Field(default=None)
    stock_splits: float | None = Field(default=None)
    ticker: str = Field(index=True, max_length=20)
    last_updated: datetime = Field(default_factory=datetime.utcnow)



print(BigInteger)