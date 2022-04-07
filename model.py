import pyupbit
import numpy as np
# from prophet import Prophet
from neuralprophet import NeuralProphet
import warnings
warnings.filterwarnings(action='ignore')

inp_hour=12
oup_hour=4

def get_predict_price(ticker, model_name):

    df = pyupbit.get_ohlcv(ticker, interval="minute10", count=6*inp_hour)
    df = df.reset_index()
    df['ds'] = df['index']
    df['y'] = df['close']
    data = df[['ds','y']]
    
    if model_name=="np":
        model = NeuralProphet()
    elif model_name=="p":
        model = Prophet()
        
    model.fit(data)
    
    future = model.make_future_dataframe(data, periods=6*oup_hour)
    forecast = model.predict(future)
    
    if model_name=="np":
        pred = forecast[["ds","yhat1"]]
    elif model_name=="p":
        pred = forecast[["ds","yhat"]]
    
    predicted_price=pred.mean().values[0]
    # predicted_price=pred.min()[1]
    
    return predicted_price