import sqlalchemy
import pandas as pd
from typing import Literal

_Modes = Literal['replace','append']
def push_to_db(df: pd.DataFrame, mode: _Modes = 'append'):
    try:
        # database credentials nad connection engine
        database_name = "clients_db"
        user_name = "my_user"
        password = "my_password"
        engine = sqlalchemy.create_engine(f"mysql+pymysql://{user_name}:{password}@db/{database_name}")
        # push dataframe to database
        df.to_sql('data_table', engine, if_exists=mode, index=False)
    except:
        raise Exception("Database connection error")

def pull_from_db() -> pd.DataFrame:
    try:
        # database credentials nad connection engine
        database_name = "clients_db"
        user_name = "my_user"
        password = "my_password"
        engine = sqlalchemy.create_engine(f"mysql+pymysql://{user_name}:{password}@db/{database_name}")
        table_name = "data_table"
        # database query
        query = f'SELECT * FROM {table_name}'
        # read database to dataframe
        df = pd.read_sql(query, engine)
        # return dataframe
        return df
    except:
        raise Exception("Database connection error")
