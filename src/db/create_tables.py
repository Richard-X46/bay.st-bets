from sqlmodel import SQLModel, text
from db.config import engine
from db.models import ExchangeIndexes, EquityPriceHistory  # Import the model to register it with Base


with engine.connect() as conn:
    result = conn.execute(text("SELECT current_database();"))
    print("Connected to DB:", result.fetchone()[0])

# creating tables with SQLModel, if they dones't exist

# for new columns and changes in models - refer to alembic migrations


# droping tables - testing purpose only

ExchangeIndexes.__table__.drop(engine)
EquityPriceHistory.__table__.drop(engine)

# create tables
SQLModel.metadata.create_all(engine)
print(ExchangeIndexes.__table__.c.marketCap.type)