import ezibpy
import time
from csvhandler import CSVHandler

class IBHandler():
    def __init__(self):
        keys = {'gateway': {'paper': 4002, 'live': 4001}, 'tws': {'paper': 7497, 'live': 7496}}
        self.connection = ezibpy.ezIBpy()
        self.connection.connect(clientId=1, port=keys['gateway']['paper'])

    def request_historical_data(self, ticker, intervalOfSeconds, endDatetime):
        self.connection.createStockContract(ticker)
        self.connection.requestHistoricalData(resolution="1 secs", lookback=f"{intervalOfSeconds} S",
                                              csv_path=CSVHandler().datapath, end_datetime=endDatetime)
        try:
            while True:
                time.sleep(10)
                return True
        except (KeyboardInterrupt, TimeoutError, SystemExit):
            self.connection.cancelHistoricalData()
            return False
