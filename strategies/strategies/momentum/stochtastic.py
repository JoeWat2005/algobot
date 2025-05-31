from strategies.base import Strategy
import pandas as pd

class StochasticOscillatorStrategy(Strategy):
    def __init__(self, k_period=14, d_period=3):
        self.k_period = k_period
        self.d_period = d_period

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()

        # Flatten MultiIndex columns if present
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        print("\n[StochasticOscillatorStrategy] Input index:", type(df.index))
        print("[StochasticOscillatorStrategy] Input head:")
        print(df.head(3))

        # Stochastic Oscillator calculation
        low_min = df['Low'].rolling(window=self.k_period).min()
        high_max = df['High'].rolling(window=self.k_period).max()
        df['%K'] = 100 * ((df['Close'] - low_min) / (high_max - low_min))
        df['%D'] = df['%K'].rolling(window=self.d_period).mean()

        # Signal generation
        df['signal'] = 0
        df.loc[df['%K'] > df['%D'], 'signal'] = 1
        df.loc[df['%K'] < df['%D'], 'signal'] = -1

        # Debugging output
        print("[StochasticOscillatorStrategy] signal counts:\n", df['signal'].value_counts())
        print("[StochasticOscillatorStrategy] Sample %K and %D:\n", df[['%K', '%D']].dropna().head(3))

        return df
