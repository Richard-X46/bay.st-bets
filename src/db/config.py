from sqlmodel import create_engine, Session,text
from dotenv import load_dotenv
import os


load_dotenv()

connection_params = {
    "user": os.getenv("PSQL_USER"),
    "password": os.getenv("PSQL_PASSWORD"),
    "host": os.getenv("PSQL_HOST"),
    "port": os.getenv("PSQL_PORT"),
    "dbname": os.getenv("DBNAME"),
}



# Create the SQLAlchemy engine using connection parameters
engine = create_engine("postgresql+psycopg2://", connect_args=connection_params)


# list all tables
def list_tables():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema='public';"))
        tables = result.fetchall()
        return [table[0] for table in tables]

list_of_tables = list_tables()
print("Tables in the database:", list_of_tables)

def get_session():
    return Session(engine)

