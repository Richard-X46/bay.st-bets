"""
Base file for CRUD operations on the database.

"""

from db.models import ExchangeIndexes
from sqlmodel import Session,select,text
from db.config import engine



# get all symbols for a given exchange
def get_all_symbols_for_exchange(session: Session, exchange_code: str):
    """Return a list of all ticker symbols for a given exchange."""

    statement = select(ExchangeIndexes.symbol).where(ExchangeIndexes.exchange == exchange_code)
    return [row for row in session.exec(statement)]


# get tickers present in equity_price_history
def get_tickers_in_price_history(session: Session):
    """Return a list of all ticker symbols present in equity_price_history table."""

    statement = select(ExchangeIndexes.symbol).where(
        ExchangeIndexes.symbol.in_(
            select(text("DISTINCT ticker")).select_from(text("equity_price_history"))
        )
    )
    return [row for row in session.exec(statement)]





# testing text 
def test_raw_sql(session: Session):
    """Test raw SQL execution."""
    result = session.exec(text("SELECT COUNT(*) FROM exchange_indexes;"))
    count = result.fetchone()[0]
    return count






# testing crud operations
if __name__ == "__main__":
    with Session(engine) as session:
        symbols = get_all_symbols_for_exchange(session, "TOR")
        print(f"Symbols for TOR exchange: {symbols}")

        count = test_raw_sql(session)
        print(f"Total records in exchange_indexes: {count}")