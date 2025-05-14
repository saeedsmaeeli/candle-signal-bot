import yfinance as yf
import pandas as pd
import datetime

def detect_candle_patterns(df):
    signals = []
    for i in range(1, len(df)):
        prev = df.iloc[i - 1]
        curr = df.iloc[i]
        if curr['Close'] > curr['Open'] and prev['Close'] < prev['Open'] and \
           curr['Close'] > prev['Open'] and curr['Open'] < prev['Close']:
            signals.append('Bullish Engulfing')
        elif curr['Close'] < curr['Open'] and prev['Close'] > prev['Open'] and \
             curr['Open'] > prev['Close'] and curr['Close'] < prev['Open']:
            signals.append('Bearish Engulfing')
        else:
            signals.append(None)
    signals.insert(0, None)
    df['Candle Pattern'] = signals
    return df

def volume_confirmation(df):
    df['Volume_MA'] = df['Volume'].rolling(window=20).mean()
    df['Volume_Confirmed'] = df['Volume'] > df['Volume_MA']
    return df

def generate_signals(df):
    df['Signal'] = None
    for i in range(len(df)):
        if df['Candle Pattern'].iloc[i] == 'Bullish Engulfing' and df['Volume_Confirmed'].iloc[i]:
            df.at[i, 'Signal'] = 'Buy'
        elif df['Candle Pattern'].iloc[i] == 'Bearish Engulfing' and df['Volume_Confirmed'].iloc[i]:
            df.at[i, 'Signal'] = 'Sell'
    return df

def run_bot(ticker='AAPL', start_date='2023-01-01'):
    df = yf.download(ticker, start=start_date)
    df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
    df = detect_candle_patterns(df)
    df = volume_confirmation(df)
    df = generate_signals(df)
    signals = df[df['Signal'].notnull()]
    print(f"\n📈 Signals for {ticker}:")
    print(signals[['Close', 'Volume', 'Candle Pattern', 'Signal']].tail(10))

if __name__ == "__main__":
    run_bot('AAPL')
