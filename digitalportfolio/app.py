from csvhandler import CSVHandler
from ibhandler import IBHandler
import time
import pandas as pd
from plothandler import PlotHandler
import numpy as np

print("""--------- COPYRIGHT William Rodman 2020 ---------

--- Rights ---
The following scripts have all been writen solely by William Rodman with the exception of the cited language.
Under my Interactive Brokers subscriptions I have the right to use the following API data for all purposes.

--- Citations ---
Ran Aroussi created the low-level program of the IB API for open use (https://github.com/ranaroussi/ezibpy).
GFIS and Interactive Brokers (interactivebrokers.github.com) provided the official NYSE, NYSEARCA, and NASDAQ market data. 
BlackRock, Inc. provided the official AUM CSV file for their iShares U.S. Utilities ETF (https://www.ishares.com/us/products/239524/ishares-us-utilities-etf).

--- Purpose ---
This program was created for William Rodman's AP Computer Science digital portfolio.""")

# Establishing the parameters of the ETFs assets and liabilities
floating_AUM, fixed_AUM = CSVHandler().fetch_IDU_AUM()
IDU_expense_ratio = 0.43
intervalOfSecondsLookback = 600
endDatetime = '20200330 09:40:00 EST'
yhat_AUM = pd.DataFrame()

# Import market data from the historical server farms using the IB API
'''
ib = IBHandler()
time.sleep(3)
inx = {'passed': 0, 'failed': 0, 'exists': 0}
for ticker in floating_AUM['ticker']:
    try:
        CSVHandler().fetch_exchange_data(ticker=ticker)
        inx['exists'] += 1
        print(f"{ticker}'s requested historical data already exists as no. {inx['exists']}")
    except:
        print(f'Requesting {ticker} as {(inx["passed"] + inx["failed"] + inx["exists"] + 1)} of {floating_AUM["ticker"].count()}')
        ib.request_historical_data(ticker, intervalOfSeconds=intervalOfSecondsLookback, endDatetime=endDatetime)
        # Time function avoids server time pacing violation
        time.sleep(60)
        try:
            CSVHandler().fetch_exchange_data(ticker=ticker)
            inx['written'] += 1
            print(f"{ticker}'s requested historical data successfully wrote to local drive as no. {inx['passed']}")
        except:
            inx['failed'] += 1
            print(f"{ticker}'s requested historical data failed to write to local drive as no. {inx['failed']}")
ib.request_historical_data('IDU', intervalOfSecondsLookback, endDatetime=endDatetime)
'''

# Parsing then apriasing the funds (assets - liabilities) after market data has been written to the local drive in .csv format
for idx, row in floating_AUM.iterrows():
    try:
        exchange_df = CSVHandler().fetch_exchange_data(ticker=row['ticker']).head(n=intervalOfSecondsLookback)
        print(f"Successfully fetched {row['ticker']}'s CSV file ")
        if idx != 0:
            multiplier = float(row['shares'].replace(',', ''))
            yhat_AUM[0] = yhat_AUM[0] + (exchange_df[0].astype(float) * multiplier)
        else:
            exchange_df[0] = exchange_df[0].astype(float)
            yhat_AUM = exchange_df
    except:
        print(f"Floating asset calculation error for {row['ticker']}")
fixed_value = 0
for idx, row in fixed_AUM.iterrows():
    try:
        fixed_value += float(row['marketvalue'].replace(',', ''))
        print(f"Successfully calculated {row['ticker']}'s towards the AUM")
    except:
        print(f"Fixed asset adaptation error for {row['ticker']}")
yhat_AUM[1] = fixed_value
yhat_AUM['O'] = (yhat_AUM[0] + yhat_AUM[1]) * IDU_expense_ratio
CSVHandler().write_yhat_IDU_AUM_data(dataframe=yhat_AUM)
print('Successfully wrote AUM dataframe to a CSV file and will launch visualization in 3 seconds')
time.sleep(3)

# Normailizing the datasets being used to calc the IDU metric
def normailize_axis_data(dataframe):
    norm = np.linalg.norm(dataframe.values)
    normal_array = dataframe.values / norm
    return dataframe.index.values, normal_array
IDU_x, IDU_y = normailize_axis_data(CSVHandler().fetch_exchange_data("IDU"))
yhat_AUM_x, yhat_AUM_y = normailize_axis_data(CSVHandler().fetch_exchange_data("yhat_IDU_AUM"))
IDU_discount = []
for IDU, yhat_AUM in zip(IDU_y, yhat_AUM_y):
    IDU_discount.append(IDU - yhat_AUM)

#Visualize the ETF's discount for every second
print('Discount metric will be plotted on graph check your desktop to see graph')
PlotHandler(x=IDU_x, y=IDU_discount)
