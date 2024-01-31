import pandas_ta as ta
import pandas as pd
from datetime import date


import os

def get_bollinger_bands(data, window=20, num_std_dev=2):
    bbands = ta.bbands(data['Close'], length=window, std=num_std_dev)
    return bbands

def get_signal(data, window=20, num_std_dev=2):
    bbands = get_bollinger_bands(data, window, num_std_dev)
    current_close = data['Close'].iloc[-1]
    
    if current_close < bbands['BBL_20_2.0'].iloc[-1]:
        signal = "Buy"
    elif current_close > bbands['BBU_20_2.0'].iloc[-1]:
        signal = "Sell"
    else:
        signal = "Neutral"
    
    return signal, current_close

def calculate_return(data, signal):
    returns = data['close'].pct_change().dropna()
    
    # Extract the signal string from the tuple
    signal_string = signal[0]

    buy_returns = returns[signal_string == "Buy"]
    sell_returns = returns[signal_string == "Sell"]
    
    total_return = (1 + buy_returns).prod() / (1 + sell_returns).prod()
    
    return (total_return - 1) * 100

def calculate_average_duration(signal):
    signal_changes = (signal[0] != signal[0].shift()).astype(int)
    durations = signal_changes.groupby(signal_changes.cumsum()).cumcount() + 1
    average_duration = durations.mean()
    
    return average_duration

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



def main(df):
    signal, current_close = get_signal(df)
    return signal




if __name__ == "__main__":

    stock_path = r'D:\college\fourth_sem\applied_programming\django_project\stockAnalysis\data\stockwise'
    paths = return_files(stock_path)
    
    for path_ in paths:
        if 'NABIL' not in path_:
            continue

        df = pd.read_csv(path_)
        df = parse_df(df)
        print(df)

        signal = main(df)
        print(signal)

