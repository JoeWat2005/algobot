from strategies.base import Strategy
import pandas as pd

class BollingerBandsStrategy(Strategy):
    def __init__(self, window=20, num_std=2):
        self.window = window
        self.num_std = num_std

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()

        # Flatten columns if MultiIndex
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        print("\n[BollingerBandsStrategy] Input index:", type(df.index))
        print("[BollingerBandsStrategy] Input head:")
        print(df.head(3))

        # Calculate moving average and standard deviation
        ma = df['Close'].rolling(self.window).mean()
        std = df['Close'].rolling(self.window).std()

        upper_band = ma + self.num_std * std
        lower_band = ma - self.num_std * std

        # Align everything to Close for safe comparison
        close, upper_band = df['Close'].align(upper_band, axis=0)
        _, lower_band = df['Close'].align(lower_band, axis=0)

        df['ma'] = ma
        df['upper_band'] = upper_band
        df['lower_band'] = lower_band

        df['signal'] = 0
        df.loc[close < lower_band, 'signal'] = 1
        df.loc[close > upper_band, 'signal'] = -1

        print("[BollingerBandsStrategy] signal counts:\n", df['signal'].value_counts())

        return df
