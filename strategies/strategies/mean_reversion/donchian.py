from strategies.base import Strategy
import pandas as pd

class DonchianChannelStrategy(Strategy):
    def __init__(self, window=20):
        self.window = window

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()
        df['upper_channel'] = df['High'].rolling(self.window).max()
        df['lower_channel'] = df['Low'].rolling(self.window).min()
        df['signal'] = 0
        df.loc[df['Close'] > df['upper_channel'], 'signal'] = -1
        df.loc[df['Close'] < df['lower_channel'], 'signal'] = 1
        return df
