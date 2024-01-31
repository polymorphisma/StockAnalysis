import pandas as pd
import os
from datetime import date

from generate_today_signal.boolinger import main as boolinger_today_signal
from generate_today_signal.ema import main as ema_today_signal
from generate_today_signal.macd import main as macd_today_signal
from generate_today_signal.momentum import main as momentum_today_signal
from generate_today_signal.rsi import main as rsi_today_signal
from generate_today_signal.sma import main as sma_today_signal
from generate_today_signal.stochrsi import main as stochrsi_today_signal

class SignalGenerator:
    def __init__(self) -> None:
        self.indicator_dict = {
            'boolinger':{
                'signal':boolinger_today_signal #CHATGPT SIGNAL
            },
            'ema':{
                'signal':ema_today_signal #CHATGPT SIGNAL
            },
            'macd':{
                'signal':macd_today_signal #CHATGPT SIGNAL
            },
            'momentum':{
                'signal':momentum_today_signal #CHATGPT SIGNAL
            },
            'rsi':{
                'signal':rsi_today_signal #CHATGPT SIGNAL
            },
            'sma':{
                'signal':sma_today_signal #CHATGPT SIGNAL
            },
            
            'stochrsi':{
                'signal':stochrsi_today_signal #CHATGPT SIGNAL
            },
        }


    def execute(self, df):
        print(df)

        temp_dict = {}

        for key, value in self.indicator_dict.items():
            signal = value['signal'](df)
            
            
            temp_dict[key] = signal

        return temp_dict


def return_files(path_, fullpath = True):
    if fullpath:
        return [os.path.join(path_, x) for x in os.listdir(path_)]
    return [x for x in os.listdir(path_)]

def parse_df(df):
    columns = {
        'BUSINESS_DATE':'date',
        "SYMBOL":"ticker",
        "OPEN_PRICE": "open",
        "HIGH_PRICE": 'high',
        "LOW_PRICE": 'low',
        "CLOSE_PRICE": 'Close',
        "TOTAL_TRADED_QUANTITY": 'volume',
        "TOTAL_TRADED_VALUE":"value"
    }


    df.rename(columns = columns, inplace=True)

    df['date'] = pd.to_datetime(df['date'])
    

    for parse_col in list(columns.values())[2:]:
        df[parse_col] = df[parse_col].astype(float)


    return df

def return_df(path):
    df = pd.read_csv(path)
    return parse_df(df)


def main(path):
    paths = return_files(path)
    
    obj = SignalGenerator()

    temp_list = []

    for path_ in paths:
        ticker = path_.split('\\')[-1].replace('.csv', '')
        df = return_df(path_)

        try:
            signals = obj.execute(df)
        except Exception as exp:
            continue
        
        signals["ticker"] = ticker
        temp_list.append(signals)

    df = pd.DataFrame(temp_list)
    
    return df

if __name__ == '__main__':
    stock_path = r'D:\college\fourth_sem\applied_programming\django_project\stockAnalysis\data\stockwise'
    
    df = main(stock_path)
    

    # df['updated_date'] = '2023-01-30'
    df['updated_date'] = str(date.today())


    from Database import Database
    datbase_obj = Database()

    datbase_obj.insert_database(df, 'app_stocksignal')


    