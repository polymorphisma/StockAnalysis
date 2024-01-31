import pandas as pd
from datetime import date, timedelta

def main(df: pd.DataFrame):
    df = df['_trades']
    today_date = date.today()
    timelimit = today_date - timedelta(days=3)
    if df['ExitTime'].dt.date.iloc[-1] < timelimit:
        return "Neutral"

    if df['Size'].iloc[-1] > 0:
        return "Buy"
    
    else:
        return "Sell"
    

if __name__ == '__main__':
    main()