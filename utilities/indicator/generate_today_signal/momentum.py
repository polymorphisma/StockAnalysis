import pandas_ta as ta
import pandas as pd
from datetime import date

def indicator(data, pct_change_period):
    return data.pct_change(periods=pct_change_period) * 100

def get_signal(data, pct_change_period=7, pct_change_sell=0, pct_change_buy=5):
    pct_change = indicator(data['Close'], pct_change_period)
    current_change = pct_change.iloc[-1]
    
    if current_change < pct_change_sell:
        signal = "Sell"
    elif current_change > pct_change_buy:
        signal = "Buy"
    else:
        signal = "Neutral"
    
    return signal, current_change

def calculate_return(data, signal):
    returns = data['Close'].pct_change().dropna()
    
    # Extract the signal string from the tuple
    signal_string = signal[0]
    
    # Apply the signal to all elements in the Series
    signal_condition = (signal_string == "Buy") | (signal_string == "Sell")
    buy_returns = returns[signal_condition]
    
    total_return = (1 + buy_returns).prod()
    
    return (total_return - 1) * 100

def calculate_average_duration(signal):
    signal_changes = (signal[0] != signal[0].shift()).astype(int)
    durations = signal_changes.groupby(signal_changes.cumsum()).cumcount() + 1
    average_duration = durations.mean()
    
    return average_duration


def main(df):
    signal, current_close = get_signal(df)
    return signal



