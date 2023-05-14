import yfinance as yf
import pandas as pd
from talib import RSI
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

# Downloading TSLA price data from yahoo finance.
# Note: Yahoo Finance currently limits historical data downloads depending on the resolution of data required
# The limit for 15min interval is : last 60 days
data = yf.download("TSLA", period='60d', interval="15m")
tsla_df = pd.DataFrame(data)


class RSICross(Strategy):
    data = None
    rsi = None
    close = None

    def init(self):
        # Initial data and RSI values
        self.data = tsla_df
        close = self.data['Close']
        self.rsi = self.I(RSI, close, 14)

    def next(self):
        # Evaluate strategy
        # if RSI value cross under 30 bound we open position
        if crossover(30, self.rsi) and self.position.size == 0:
            self.buy()
        # if RSI value cross over 50 bound we close the position
        elif crossover(self.rsi, 50):
            self.position.close()


# Backtest our class
bt = Backtest(tsla_df, RSICross, commission=.00,
              exclusive_orders=True)

if __name__ == '__main__':
    stats = bt.run()
    trades = stats['_trades']
    trades_log = pd.concat([trades['EntryPrice'],
                            trades['ExitPrice'],
                            trades['EntryTime'],
                            trades['ExitTime']], axis=1)

    print(trades_log)

    bt.plot()
