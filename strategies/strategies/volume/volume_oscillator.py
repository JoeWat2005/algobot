from strategies.base import Strategy
import pandas as pd

class VolumeOscillatorStrategy(Strategy):
    def __init__(self, short_period=5, long_period=20):
        self.short_period = short_period
        self.long_period = long_period

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()

        # Flatten MultiIndex columns if necessary
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        print("\n[VolumeOscillatorStrategy] Input index:", type(df.index))
        print("[VolumeOscillatorStrategy] Input head:")
        print(df.head(3))

        # Calculate short and long volume averages
        df['vol_short'] = df['Volume'].rolling(window=self.short_period).mean()
        df['vol_long'] = df['Volume'].rolling(window=self.long_period).mean()

        # Compute volume oscillator
        df['volume_osc'] = df['vol_short'] - df['vol_long']

        # Generate signals
        df['signal'] = 0
        df.loc[df['volume_osc'] > 0, 'signal'] = 1
        df.loc[df['volume_osc'] < 0, 'signal'] = -1

        # Debug output
        print("[VolumeOscillatorStrategy] signal counts:\n", df['signal'].value_counts())

        return df
