from strategies.base import Strategy
import pandas as pd

class DonchianChannelStrategy(Strategy):
    def __init__(self, window=20):
        self.window = window

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        print("\n[DonchianChannelStrategy] Input index:", type(df.index))
        print("[DonchianChannelStrategy] Input head:")
        print(df.head(3))

        upper_channel = df['High'].rolling(self.window).max()
        lower_channel = df['Low'].rolling(self.window).min()

        upper_channel, close = upper_channel.align(df['Close'], axis=0)
        lower_channel, _ = lower_channel.align(df['Close'], axis=0)

        df['upper_channel'] = upper_channel
        df['lower_channel'] = lower_channel

        df['signal'] = 0
        df.loc[close > upper_channel, 'signal'] = 1   # Buy breakout
        df.loc[close < lower_channel, 'signal'] = -1  # Sell breakdown

        print("[DonchianChannelStrategy] signal counts:\n", df['signal'].value_counts())

        return df
