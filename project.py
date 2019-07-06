# -*- coding: utf-8 -*-
"""
Created on Sat Jun 29 16:51:32 2019

@author: Jis_Mathew
"""

import pandas as pd
import numpy as np

from keras.layers import LSTM
from keras.layers import Dense
from keras.models import Sequential
from keras.optimizers import SGD
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

share=pd.read_csv('FINAL_FROM_DF.csv')
company_df=share['SYMBOL']
company_df=pd.unique(company_df)
company_list=list(company_df)
#company_list=['INFY']
per_40={}

for company,i in zip(company_list,range(len(company_list))):
    if i==20:
        break
    company_price=share[share['SYMBOL']==company]
    high=company_price['CLOSE']
    high=high.values
    high=high.reshape(-1,1)
    sc=MinMaxScaler()
    

    Xtrain=sc.fit_transform(high)
    length=len(high)
    X_train=Xtrain[0:length-2]
    
    y_train=Xtrain[1:length-1]

    X_train=X_train.reshape(length-2,1,1)

    regressor=Sequential()

    regressor.add(LSTM(units=1000,activation='sigmoid',input_shape=(None,1)))
    regressor.add(Dense(units=1))
    regressor.compile(optimizer='adam',loss='mean_squared_error')

    regressor.fit(X_train,y_train,batch_size=32,epochs=30,verbose=0)

    testlen=20
    testdata=high[0-testlen:-1]
    inputs=sc.transform(testdata)
    inputs=inputs.reshape(testlen-1,1,1)

    pre=regressor.predict(inputs)
    pre=sc.inverse_transform(pre)
    ori=high[0-testlen:]

    inputs=inputs.reshape(testlen-1,1)

    mse=0
    count=0
    for x,y in zip(pre.flatten(),ori.flatten()):
        error=y-x
        error=error*error
        mse=mse+error
        count=count+1
    mse=mse/count
    rmse=mse**0.5
    average_ori=ori.sum()/len(ori)
    percentile=rmse/average_ori
    percentile*=100
    print('company Count',i+1)
    print('Number of observations: ',length)
    print ('Company : ',company)
    print('Average Stock Price: ',average_ori)
    print('Mean square error: ',mse)
    print('Root Mean square error: ',rmse)
    print('Percentile Error: ',percentile)
    print('------------------------------------------------------------')
    per_40[company]=percentile