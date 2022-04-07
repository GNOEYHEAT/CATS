import pyupbit
import time
import datetime
import numpy as np


def get_current_price(ticker):
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]

def get_target_price(ticker, target_interval, k):
    df = pyupbit.get_ohlcv(ticker, interval=target_interval, count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_ma(ticker, ma_interval, ma_count):
    df = pyupbit.get_ohlcv(ticker, interval=ma_interval, count=ma_count)
    ma = df['close'].rolling(ma_count).mean().iloc[-1]
    return ma

def get_balance(ticker, account):
    balances = account.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_ror(ticker, k):
    df = pyupbit.get_ohlcv(ticker, interval='minute10', count=6*24)
    time.sleep(0.1)
    df['range'] = (df['high'] - df['low']) * k
    df['target'] = df['open'] + df['range'].shift(1)
    df['ror'] = np.where(df['high'] > df['target'],
                         df['close'] / df['target'],
                         1)
    ror = df['ror'].cumprod()[-2]
    return ror

def get_k(ticker):
    temp_k=0
    temp_ror=0
    for k in np.arange(0.1, 1.0, 0.1):
        k=k.round(2)
        ror = get_ror(ticker, k)
        if temp_ror<ror:
            temp_k=k
            temp_ror=ror
    return temp_k