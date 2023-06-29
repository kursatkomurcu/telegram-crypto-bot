import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from sklearn.preprocessing import MinMaxScaler
import matplotlib as mpl
import matplotlib.pyplot as plt

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM

import numpy as np

look_back = 1
scaler = MinMaxScaler(feature_range=(0,1)) # normalization

def create_dataset(dataset, look_back=1):
	dataX, dataY = [], []
	for i in range(len(dataset)-look_back-1):
		a = dataset[i:(i+look_back), 0]
		dataX.append(a)
		dataY.append(dataset[i + look_back, 0])
	return np.array(dataX), np.array(dataY)

def preprocessing(name):
    name = name + "-USD"
    crypto = yf.download(name, start="2013-01-01", end=datetime.now().date())
    
    daily_data = crypto['Close']
    daily_data = pd.DataFrame(daily_data)

    train = daily_data.iloc[:int(len(daily_data.index)*0.75), :]
    test = daily_data.iloc[int(len(daily_data.index)*0.75+1):, :]

    data = np.array(daily_data).reshape(-1, 1)

    global scaler
    data = scaler.fit_transform(data)

    # %75 train %25 test 
    train = data[:int(len(data)*0.75), :]
    test = data[int(len(data)*0.75+1):, :]

    global look_back
    trainX, trainY = create_dataset(train, look_back)
    testX, testY = create_dataset(test, look_back)

    trainX = np.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
    testX = np.reshape(testX, (testX.shape[0], 1, testX.shape[1]))

    return trainX, trainY, testX, testY, data, daily_data

def trainPredict(name, n_past=30, n_days_for_prediction=30):
    global look_back
    trainX, trainY, testX, testY, data, daily_data = preprocessing(name)
    
    lstm_model = Sequential()  # lstm model
    lstm_model.add(LSTM(units=20, activation='relu', return_sequences=True, input_shape=(1, look_back)))
    lstm_model.add(LSTM(units=20, activation='relu', return_sequences=True))
    lstm_model.add(Dense(units=1))

    lstm_model.compile(optimizer='adam', loss='mean_squared_error')
    lstm_model.fit(trainX, trainY, epochs=10, batch_size=1, verbose=1)

    data = np.reshape(data, (data.shape[0], data.shape[1], -1))
    
    prediction = lstm_model.predict(data[-n_days_for_prediction:])
    prediction_copies = np.repeat(prediction, data.shape[1], axis=-1)
    prediction_copies = np.reshape(prediction_copies, (prediction_copies.shape[0], prediction_copies.shape[1]))

    global scaler
    y_pred_future = scaler.inverse_transform(prediction_copies)[:,0]

    today = datetime.now().date()
    dates = today + timedelta(days=n_days_for_prediction)

    forecast_dates = []
    for tarih in range((dates - today).days):
        forecast_dates.append(today + timedelta(days=tarih))

    y_pred_future = y_pred_future[-len(forecast_dates):]  # Limit predictions correctly

    df_forecast = pd.DataFrame({'Open Time': forecast_dates, 'Close': y_pred_future})
    df_forecast['Open Time'] = pd.to_datetime(df_forecast['Open Time'])

    return df_forecast, daily_data

def getLSTMResults(name):
    df_forecast, daily_data = trainPredict(name)

    # for 30th day
    change_percentage30 = (100 * df_forecast.iloc[-1:, 1])  / daily_data['Close'][-1]
    change_percentage30 = np.array(change_percentage30)
    change_percentage30 = change_percentage30 - 100

    # for 10th day
    change_percentage10 = (100 * df_forecast.iloc[-20:-19, 1])  / daily_data['Close'][-1]
    change_percentage10 = np.array(change_percentage10)
    change_percentage10 = change_percentage10 - 100

    # for max point
    change_percentage_max = (100 * df_forecast['Close'].max())  / daily_data['Close'][-1]
    change_percentage_max = np.array(change_percentage_max)
    change_percentage_max = change_percentage_max - 100

    # for min point
    change_percentage_min = (100 * df_forecast['Close'].min())  / daily_data['Close'][-1]
    change_percentage_min = np.array(change_percentage_min)
    change_percentage_min = change_percentage_min - 100

    # Forecating of 30th day, 10th day, max value and min value (in 30 days) 
    return df_forecast.iloc[-1:, 1], df_forecast.iloc[-20:-19, 1], df_forecast['Close'].max(), df_forecast['Close'].min(), change_percentage30, change_percentage10, change_percentage_max, change_percentage_min

