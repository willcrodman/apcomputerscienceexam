import csv
import pandas as pd

class CSVHandler:
    datapath = "/Users/willrodman/Desktop/digitalportfolio/data/"

    def fetch_exchange_data(self, ticker):
        rows = []
        data = {'datetime': [], 'open': []}
        with open(self.datapath + f"{ticker}.csv", 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            fields = next(csvreader)
            for row in csvreader:
                rows.append(row)
            for row in rows:
                data['datetime'].append(row[fields.index('datetime')])
                data['open'].append(float(row[fields.index('O')]))
        return pd.DataFrame(data['open'], index=data['datetime'])

    def fetch_IDU_AUM(self):
        rows = []
        floating = {'ticker': [], 'shares': []}
        fixed = {'ticker': [], 'marketvalue': []}
        with open(self.datapath + "IDU_AUM.csv", 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            fields = next(csvreader)
            for row in csvreader:
                rows.append(row)
        for row in rows:
            exchange = row[fields.index('Exchange')]
            ticker = row[fields.index('Ticker')]
            if exchange == "New York Stock Exchange Inc." or exchange == "NASDAQ":
                floating['ticker'].append(ticker)
                floating['shares'].append(row[fields.index('Shares')])
            else:
                fixed['ticker'].append(ticker)
                fixed['marketvalue'].append(row[fields.index('Notional Value')])
        return pd.DataFrame(floating), pd.DataFrame(fixed)

    def write_yhat_IDU_AUM_data(self, dataframe):
        if type(dataframe) == type(pd.DataFrame()):
            path = self.datapath + 'yhat_IDU_AUM.csv'
            dataframe.index.name = 'datetime'
            dataframe.fillna(value=0, inplace=True)
            dataframe.to_csv(path, index=True)
            return True
        else:
            return False