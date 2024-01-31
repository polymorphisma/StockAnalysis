import os
from sqlalchemy import create_engine, text
import psycopg2

import pandas as pd
import urllib.parse


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

import sys
sys.path.append(ROOT_DIR)

from dotenv import load_dotenv
load_dotenv()

class Database:
    USERNAME = os.environ.get('DBUSERNAME')
    PASSWORD = os.environ.get('DBPASSWORD')
    PORT = os.environ.get('DBPORT')
    DATABASE = os.environ.get('DBDATABASE')
    HOST = os.environ.get('DBHOST')

    @staticmethod
    def _generateConnection():
        conn = psycopg2.connect(host=Database.HOST, port=Database.PORT, dbname=Database.DATABASE, user=Database.USERNAME, password=Database.PASSWORD)
        engine = create_engine(f"postgresql://{Database.USERNAME}:{urllib.parse.quote_plus(str(Database.PASSWORD))}@{Database.HOST}:{Database.PORT}/{Database.DATABASE}")
        return conn, engine
    
    def insert_database(self, df, table_name, if_exists = 'append', index= False):
        _, engine = Database._generateConnection()
        df.reset_index(inplace=True, drop=True)
        if 'id' in df.columns:
            df.drop(columns=['id'], inplace=True)
        try:
            df.to_sql(table_name, engine, if_exists = if_exists, index=index) 
        except Exception as exp:
            raise exp
        
    def return_table(self, table_name):
        _, engine = Database._generateConnection()
        query = text(f"""SELECT * FROM {table_name};""")

        database_df = pd.read_sql(query, engine)
        database_df.drop(['id'], axis=1, inplace=True)

        return database_df
    
    def update_table(self, query):
        conn, _ = Database._generateConnection()

        with conn:
            with conn.cursor() as cursor:
                cursor.execute(query)


    def remove_duplicates(self, table_name, subset = []):
        # conn, engine = Database._generateConnection()
        df = self.return_table(table_name)
        df = df.drop_duplicates(subset=subset)
        self.insert_database(df, table_name, if_exists='replace', index=True)
