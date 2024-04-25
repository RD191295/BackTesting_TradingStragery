import talib
from backtesting import Strategy, Backtest
from backtesting.lib import crossover, resample_apply
import yfinance as yfi
import pandas as pd


class RsiOscillator(Strategy):

    def __init__(self, broker, data, params):
        super().__init__(broker, data, params)
        self.weekly_rsi = None
        self.lower_bound = None
        self.upper_bound = None
        self.daily_rsi = None
        self.rsi_window = 14
        self.stop_loss = 0.05
        self.take_profit = 0.1

    def init(self):
        self.upper_bound = 50
        self.lower_bound = 40

        self.daily_rsi = self.I(talib.RSI, self.data.Close, self.rsi_window)

    def next(self):
        price = self.data.Close[-1]
        if crossover(self.daily_rsi, self.upper_bound):
            self.position.close()
        elif crossover(self.lower_bound, self.daily_rsi):
            self.buy(size=.1, tp=1.15 * price, sl=0.95 * price)


# Execute Backtesting on Data

data = yfi.download(["GOOG"])

backtesting = Backtest(data, RsiOscillator, cash = 10_000, commission=.03, exclusive_orders=True)
stats = backtesting.run()
backtesting.plot()

# Convert statistics to DataFrame
stats_df = pd.DataFrame(stats)
# Store DataFrame in a CSV file
stats_df.to_csv('backtest_stats.csv')
