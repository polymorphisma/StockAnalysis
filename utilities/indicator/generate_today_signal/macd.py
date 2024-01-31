import pandas_ta as ta
import pandas as pd
from datetime import date

def get_macd(data, fast_period=12, slow_period=26, signal_period=9):
    macd = ta.macd(data['Close'], fast=fast_period, slow=slow_period, signal=signal_period)
    return macd

def get_signal(data, fast_period=12, slow_period=26, signal_period=9):
    macd = get_macd(data, fast_period, slow_period, signal_period)
    current_macd = macd.iloc[-1]  # Get the current MACD value
    
    if current_macd.iloc[0] > 0:  # Compare the first element (current MACD) with 0
        signal = "Buy"
    elif current_macd.iloc[0] < 0:  # Compare the first element (current MACD) with 0
        signal = "Sell"
    else:
        signal = "Neutral"
    
    return signal, current_macd.iloc[0]  # Return the first element (current MACD)

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


