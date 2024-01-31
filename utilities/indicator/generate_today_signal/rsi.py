import pandas_ta as ta
import pandas as pd
from datetime import date

def indicator(data, rsi_period):
    return ta.rsi(data, length=rsi_period)

def get_signal(data, rsi_period=14, overbought=70, oversold=30):
    rsi = indicator(data['Close'], rsi_period)
    current_rsi = rsi.iloc[-1]
    
    if current_rsi > overbought:
        signal = "Sell"
    elif current_rsi < oversold:
        signal = "Buy"
    else:
        signal = "Neutral"
    
    return signal, current_rsi

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



