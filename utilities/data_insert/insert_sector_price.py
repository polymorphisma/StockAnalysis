import pandas as pd
import os


from Database import Database
database_obj = Database()


def return_files(path_, fullpath = True):
    if fullpath:
        return [os.path.join(path_, x) for x in os.listdir(path_)]
    return [x for x in os.listdir(path_)]

def parse_df(df):
    columns = {
        'Date':'date',
        "Symbol":"ticker",
        "Open": "open",
        "High": 'high',
        "Low": 'low',
        "Close": 'close',
        "Volume": 'volume',
        "Value":"value"
    }


    df.rename(columns = columns, inplace=True)

    df['date'] = pd.to_datetime(df['date'])
    df['ticker'] = df['ticker'].str.upper()

    df.fillna(0, inplace=True)
    

    for parse_col in list(columns.values())[2:]:
        df[parse_col] = df[parse_col].astype(float)

    return df

def insert_in_database(df, table_name:str = 'app_stockdata'):
    database_obj.insert_database(df, table_name)


def execute(path_):
    paths = return_files(path_)
    
    for path_ in paths:
        df = pd.read_csv(path_)
        insert_in_database(parse_df(df))

if __name__ == "__main__":
    stock_path = r'D:\college\fourth_sem\applied_programming\django_project\stockAnalysis\data\sectorwise'
    execute(stock_path)

    