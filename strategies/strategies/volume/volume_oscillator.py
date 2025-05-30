from strategies.base import Strategy
import pandas as pd

class VolumeOscillatorStrategy(Strategy):
    def __init__(self, short_period=5, long_period=20):
        self.short_period = short_period
        self.long_period = long_period

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()
        df['vol_short'] = df['Volume'].rolling(window=self.short_period).mean()
        df['vol_long'] = df['Volume'].rolling(window=self.long_period).mean()
        df['volume_osc'] = df['vol_short'] - df['vol_long']
        df['signal'] = 0
        df.loc[df['volume_osc'] > 0, 'signal'] = 1
        df.loc[df['volume_osc'] < 0, 'signal'] = -1
        return df
