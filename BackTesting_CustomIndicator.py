import pandas_ta as ta
import yfinance as yfi
from backtesting import Backtest, Strategy
import pandas as pd


def indicator(data):
    """
    You can Define your custom idicator
    :param data:
    :return:
    """
    bbands = ta.bbands(close=data.Close.s, std=1)
    return bbands.to_numpy().T[0:3]


class BBStrategy(Strategy):

    def init(self):
        """

        Initalization of Parameter etc
        :return:
        """
        self.bbands = self.I(indicator, self.data)
        pass

    def next(self):
        """

        Define Your Startergy Here
        :return:
        """
        lower_band = self.bbands[0]
        upper_band = self.bbands[2]
        price = self.data.Close[-1]
        if self.position:
            if self.data.Close[-1] > upper_band[-1]:
                self.position.close()
        else:
            if self.data.Close[-1] < lower_band[-1]:
                # Take Profit : 1.3 Times of Price
                # Stop Loss : 5% price
                self.buy(tp=1.5 * price, sl=0.97 * price)


data = yfi.download(["AMZN"], start="2010-01-01", end="2024-04-20")
bt = Backtest(data, BBStrategy, cash=10000, commission=0.03,
              exclusive_orders=True)  # margin parameter can be added if margin tradding need to be done
# default margin = 1
stats = bt.run()

#ploting Graph
bt.plot()

# Convert statistics to DataFrame
stats_df = pd.DataFrame(stats)
# Store DataFrame in a CSV file
stats_df.to_csv('backtest_stats_BBAND.csv')