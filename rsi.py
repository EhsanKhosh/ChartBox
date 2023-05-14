import pandas as pd


def pandas_rsi(df: pd.DataFrame, window_length: int = 14, output: str = None, price: str = 'Close'):
    # Calculate Price Differences using the column specified as price.
    df['diff1'] = df[price].diff(1)

    # Calculate Avg. Gains/Losses
    df['gain'] = df['diff1'].clip(lower=0).round(2)
    df['loss'] = df['diff1'].clip(upper=0).abs().round(2)

    # Get initial Averages
    df['avg_gain'] = df['gain'].rolling(window=window_length, min_periods=window_length).mean()[:window_length + 1]
    df['avg_loss'] = df['loss'].rolling(window=window_length, min_periods=window_length).mean()[:window_length + 1]

    # Calculate Average Gains
    for i, row in enumerate(df['avg_gain'].iloc[window_length + 1:]):
        df['avg_gain'].iloc[i + window_length + 1] = \
            (df['avg_gain'].iloc[i + window_length] *
             (window_length - 1) +
             df['gain'].iloc[i + window_length + 1]) \
            / window_length

    # Calculate Average Losses
    for i, row in enumerate(df['avg_loss'].iloc[window_length + 1:]):
        df['avg_loss'].iloc[i + window_length + 1] = \
            (df['avg_loss'].iloc[i + window_length] *
             (window_length - 1) +
             df['loss'].iloc[i + window_length + 1]) \
            / window_length

    # Calculate RS Values
    df['rs'] = df['avg_gain'] / df['avg_loss']

    # Calculate RSI
    df['rsi'] = 100 - (100 / (1.0 + df['rs']))

    # Save if specified
    if output is not None:
        df.to_csv(output)

    return df
