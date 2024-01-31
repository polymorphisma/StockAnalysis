import pandas_ta as ta
import pandas as pd
from datetime import date

def get_ema(data, window=20):
    ema = ta.ema(data['Close'], length=window)
    return ema

def get_signal(data, window=20):
    ema = get_ema(data, window)
    current_close = data['Close'].iloc[-1]
    
    if current_close > ema.iloc[-1]:
        signal = "Buy"
    elif current_close < ema.iloc[-1]:
        signal = "Sell"
    else:
        signal = "Neutral"
    
    return signal, current_close

def calculate_return(data, signal):
    returns = data['Close'].pct_change().dropna()
    
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


def main(df):
    signal, current_close = get_signal(df)
    return signal

