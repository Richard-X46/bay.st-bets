import logging
from db.config import get_session


from db.models import ExchangeIndexes , EquityPriceHistory
from data_fetch import get_stocks_by_exchange , get_ticker_price_history
from db.crud import get_all_symbols_for_exchange , get_tickers_in_price_history
import pandas as pd
import time
from sqlalchemy.dialects.postgresql import insert

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)



# ---/// Store exchange data \\\ ---
def store_exchange_data(exchange_code: str):
    db = get_session()

    df = get_stocks_by_exchange(exchange_code)
    for idx, row in df.iterrows():
        try:
            record = row.to_dict()
            logger.info(f"Storing record for {idx,record['symbol']} - remaining: {len(df)-idx}")
            
            row.to_dict()

            insert_query = insert(ExchangeIndexes).values(**record)
            upsert_query = insert_query.on_conflict_do_update(
                index_elements=['symbol'],
                set_={key: record[key] for key in record if key != 'symbol'}
            )
            db.exec(upsert_query)

             
        except Exception as e:
            logger.error(f"Failed on row {idx}: {row.to_dict()}")
            logger.error(f"Error: {e}")
            raise
    db.commit()
    db.close() 
    logger.info(f"Data for exchange {exchange_code} stored successfully.")


# ---/// Store ticker price history \\\ ---
def store_ticker_price_history(exchange_code: str):
    db = get_session()
    try:
        ticker_list = get_all_symbols_for_exchange(db, exchange_code)

        # get tickers already present in equity_price_history to avoid redundant fetches
        existing_tickers = get_tickers_in_price_history(db)

        # 
        ticker_list = [t for t in ticker_list if t not in existing_tickers] # remove 

        

        logger.info(f"Fetched {len(ticker_list)} tickers for exchange {exchange_code}.")



        # ticker_list = ticker_list[:5]  # limit for testing

        for idx,t in enumerate(ticker_list):
            try:
                price_history_df = get_ticker_price_history(t)
                price_history_df["last_updated"] = pd.Timestamp.now()
                price_history_df["date"] = pd.to_datetime(price_history_df["date"])
                # print(price_history_df.head(), price_history_df.info())
                # bulk insert into equity_price_history table
                records = price_history_df.to_dict(orient="records")
                insert_query = insert(EquityPriceHistory).values(records)
                upsert_query = insert_query.on_conflict_do_nothing(
                    index_elements=['ticker', 'date']
                )
                db.exec(upsert_query)



                logger.info(f"Stored price history for {idx,t} - remaining: {len(ticker_list)-idx}")
                logger.info(f"ticker {t} - days {len(price_history_df)} min date {price_history_df['date'].min()} max date {price_history_df['date'].max()}")
                db.commit()
            except Exception as e:
                logger.error(f"Failed to store price history for ticker {t}: {e}")
                db.rollback()  # Reset transaction so future operations work
                continue # Skip to next ticker on error
            time.sleep(1)  # To avoid hitting API rate limits
        logger.info(f"Ticker price history for exchange {exchange_code} stored successfully.")

    except Exception as e:
        logger.error(f"Error storing ticker price history: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":

    store_exchange_data("TOR")
    # store_ticker_price_history("TOR")
    pass