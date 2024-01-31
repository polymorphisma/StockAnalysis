import pandas_ta as ta
import pandas as pd
from datetime import date

def indicator(data, rsi_period, stoch_period):
    rsi = ta.rsi(data, length=rsi_period)
    stoch_rsi = ta.stochrsi(rsi, length=stoch_period)
    return stoch_rsi

def get_signal(data, rsi_period=14, stoch_period=14, overbought=0.8, oversold=0.2):
    stoch_rsi = indicator(data['Close'], rsi_period, stoch_period)
    current_stoch_rsi = stoch_rsi.iloc[-1]
    
    if current_stoch_rsi.iloc[0] > overbought:
        signal = "Sell"
    elif current_stoch_rsi.iloc[0] < oversold:
        signal = "Buy"
    else:
        signal = "Neutral"
    
    return signal, current_stoch_rsi.iloc[0]

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


