import pandas_ta as ta
import pandas as pd
from datetime import date

def SMA(values, n):
    return pd.Series(values).rolling(n).mean()

def get_signal(df, n1=10, n2=50):
    
    # Calculate the most recent moving averages
    sma1 = SMA(df['Close'], n1)
    sma2 = SMA(df['Close'], n2)
    
    # Get the most recent closing price
    current_close = df['Close'].iloc[-1]
    
    # Check for the crossover signal
    if sma1.iloc[-1] > sma2.iloc[-1]:
        signal = "Buy"
    elif sma2.iloc[-1] > sma1.iloc[-1]:
        signal = "Sell"
    else:
        signal = "Neutral"
    
    return signal, current_close

# def backtesting()

# def calculate_accuracy(ticker, start_date, end_date, n1=10, n2=50):
#     df = yf.download(ticker, start=start_date, end=end_date)
#     signals = []
    
#     for i in range(n2, len(df)):
#         sma1 = SMA(df['Close'].iloc[i - n2:i], n1)
#         sma2 = SMA(df['Close'].iloc[i - n2:i], n2)
        
#         if sma1.iloc[-1] > sma2.iloc[-1]:
#             signals.append("Buy")
#         elif sma2.iloc[-1] > sma1.iloc[-1]:
#             signals.append("Sell")
#         else:
#             signals.append("Neutral")
    
#     correct_signals = [1 if s == signals[i+1] else 0 for i, s in enumerate(signals[:-1])]
#     accuracy = sum(correct_signals) / len(correct_signals)
    
#     return accuracy

# def calculate_average_duration(ticker, start_date, end_date, n1=10, n2=50):
#     df = yf.download(ticker, start=start_date, end=end_date)
#     signals = []
    
#     for i in range(n2, len(df)):
#         sma1 = SMA(df['Close'].iloc[i - n2:i], n1)
#         sma2 = SMA(df['Close'].iloc[i - n2:i], n2)
        
#         if sma1.iloc[-1] > sma2.iloc[-1]:
#             signals.append("Buy")
#         elif sma2.iloc[-1] > sma1.iloc[-1]:
#             signals.append("Sell")
#         else:
#             signals.append("Neutral")
    
#     # Calculate the durations between signals
#     durations = [1] * len(signals)  # Initialize with 1 to handle first signal
#     for i in range(1, len(signals)):
#         if signals[i] != signals[i - 1]:
#             durations[i] = 0
#         durations[i] += durations[i - 1]
    
#     total_duration = durations[-1]
#     total_trades = len(durations)
    
#     # Calculate the average duration
#     if total_trades > 0:
#         average_duration = total_duration / total_trades
#     else:
#         average_duration = 0
    
#     return average_duration

# def return_df(ticker, start_day, end_day):
#     df = yf.download(ticker, start=start_day, end=end_day)
#     return df



def main(df):
    signal, current_close = get_signal(df)
    return signal


