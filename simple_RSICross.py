import yfinance as yf
import pandas as pd
from rsi import pandas_rsi

data = yf.download("TSLA", period='60d', interval="15m")
tsla_df = pd.DataFrame(data)


def simple_RSICross(df):
    # Downloading TSLA price data from yahoo finance.
    # Note: Yahoo Finance currently limits historical data downloads depending on the resolution of data required
    # The limit for 15min interval is : last 60 days

    rsi = pandas_rsi(df)

    entry_price = []
    entry_time = []
    exit_price = []
    exit_time = []
    in_position_flag = False

    for i in range(len(rsi) - 1):

        if rsi['rsi'][i] > 30 > rsi['rsi'][i + 1] and not in_position_flag:
            in_position_flag = True
            entry_price.append(rsi['Close'][i + 1])
            entry_time.append(rsi.index[i + 1])

        if rsi['rsi'][i] < 50 < rsi['rsi'][i + 1] and in_position_flag:
            in_position_flag = False
            exit_price.append(rsi['Close'][i + 1])
            exit_time.append(rsi.index[i + 1])

    log_df = pd.DataFrame({'EntryPrice': entry_price, 'ExitPrice': exit_price,
                           'EntryTime': entry_time, 'ExitTime': exit_time})

    return log_df


if __name__ == '__main__':
    # View Result
    print(simple_RSICross(tsla_df))
