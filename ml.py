from logging import makeLogRecord
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller
import itertools
import warnings
warnings.filterwarnings('ignore') 
import seaborn as sns
from statsmodels.graphics.tsaplots import plot_acf,plot_pacf

data=pd.read_csv('F:\project\Superstore.csv',encoding='windows-1252',parse_dates=['Order Date'])
print(data.head())
print("----------------------------------------------------------------------------------------")
print(data.columns)
print("----------------------------------------------------------------------------------------")
print(data['Category'].unique())
print("----------------------------------------------------------------------------------------")
print(data.groupby('Category')['Sales'].count())
print("----------------------------------------------------------------------------------------")
print(data.isnull().sum())
print("----------------------------------------------------------------------------------------")
corr = data.corr()
sns.heatmap(corr, annot=True, square=True)
plt.yticks(rotation=0)
plt.show()

data.boxplot()
plt.show()

df=data[data.Category=="Furniture"].sort_values('Order Date')
print(df.head())

print("----------------------------------------------------------------------------------------")

df=df.loc[:,df.columns.isin(['Order Date','Sales'])].reset_index(drop=True)
print(df.head())

print("----------------------------------------------------------------------------------------")

df=df.groupby('Order Date')['Sales'].sum().reset_index()
print(df.head())

print("----------------------------------------------------------------------------------------")

df=df.set_index('Order Date')
print(df.index)

print("----------------------------------------------------------------------------------------")

y=df['Sales'].resample('MS').mean()
print(y[0:15])


print("----------------------------------------------------------------------------------------")

y.plot()
plt.show()

print(len(y))
y_train=y[:len(y)-11]
y_test=y[(len(y)-11):]
print(y_train[-2:])

print("----------------------------------------------------------------------------------------")

y_train.plot()
plt.show()
y_test.plot()
plt.show()

result=adfuller(y_train)
print('ADF Statistic: %f' % result[0])
print('p-value: %f' % result[1])
print('Critical Values:')

for key,value in result[4].items():
  print('\t%s: %.3f' % (key,value))

print("----------------------------------------------------------------------------------------")



ts_decomp = sm.tsa.seasonal_decompose(y_train,model='additive')
ts_decomp.plot()
plt.show()

p = d = q = range(0,2)
pdq = list(itertools.product(p,d,q))
seasonal_pdq = [(x[0],x[1],x[2],12) for x in list(itertools.product(p,d,q))]

print('Examples of parameter combinations for Seasonal ARIMA')
print('SARIMAX: {} X {}'.format(pdq[1], seasonal_pdq[1]))
print('SARIMAX: {} X {}'.format(pdq[1], seasonal_pdq[2]))
print('SARIMAX: {} X {}'.format(pdq[2], seasonal_pdq[3]))
print('SARIMAX: {} X {}'.format(pdq[2], seasonal_pdq[4]))
print('SARIMAX: {} X {}'.format(pdq[3], seasonal_pdq[5]))

print("----------------------------------------------------------------------------------------")
metric_aic_dict=dict()

for pm in pdq:
  for pm_seasonal in seasonal_pdq:
    try:
      model=sm.tsa.statespace.SARIMAX(y_train,
                                      order=pm,
                                      seasonal_order=pm_seasonal,
                                      enforce_stationary=False,
                                      enforce_invertibility=False)
      model_aic = model.fit()
      print('ARIMA{}X{}12 - AIC:{}'.format(pm, pm_seasonal, model_aic.aic))
      metric_aic_dict.update({(pm,pm_seasonal):model_aic.aic})

    except:
      continue

print("----------------------------------------------------------------------------------------")
print({k: v for k, v in sorted(metric_aic_dict.items(), key=lambda x: x[1])} )

print("----------------------------------------------------------------------------------------")
model= sm.tsa.statespace.SARIMAX(y_train,
                                 order=(0,1,1),
                                 seasonal_order=(0,1,1,12),
                                 enforce_stationary=False,
                                 enforce_invertibility=False)
model_aic = model.fit()
print(model_aic.summary().tables[1])
print("----------------------------------------------------------------------------------------")

model_aic.plot_diagnostics(figsize=(16,8))
plt.show()

forecast = model_aic.get_prediction(start=pd.to_datetime('2017-02-01'),dynamic=False)
predictions=forecast.predicted_mean

actual = y_test['2017-02-01':]

rmse= np.sqrt((predictions - actual) ** 2).mean()
print('The Root Mean Squared Error of our forecasts is {}'.format(round(rmse,2)))

print("----------------------------------------------------------------------------------------")

forecast = model_aic.get_forecast(steps=24)

predictions = forecast.predicted_mean
ci= forecast.conf_int()

fig = y.plot(label = 'observed', figsize=(14,7))
fig.set_xlabel('Date')
fig.set_ylabel('Sales')
fig.fill_between(ci.index,
                 ci.iloc[:,0],
                 ci.iloc[:,1], color='k', alpha=.2)

predictions.plot(ax=fig, label='Predictions',alpha=.7,figsize=(14,7))

plt.legend()
plt.show()