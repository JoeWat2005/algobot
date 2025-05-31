from strategies.base import Strategy
import pandas as pd

class ZScoreStrategy(Strategy):
    def __init__(self, period=20, threshold=1.5):
        self.period = period
        self.threshold = threshold

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()

        # Flatten columns if MultiIndex
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        print("\n[ZScoreStrategy] Input index:", type(df.index))
        print("[ZScoreStrategy] Input head:")
        print(df.head(3))

        # Compute rolling mean and std
        mean = df['Close'].rolling(self.period).mean()
        std = df['Close'].rolling(self.period).std()

        # Ensure mean/std are aligned with df
        mean, _ = mean.align(df['Close'], axis=0)
        std, _ = std.align(df['Close'], axis=0)

        # Compute z-score
        zscore = (df['Close'] - mean) / std

        # Debug: check if zscore is a Series
        print("[ZScoreStrategy] zscore type:", type(zscore))

        df['signal'] = 0
        df['mean'] = mean
        df['std'] = std
        df['zscore'] = zscore

        df.loc[df['zscore'] > self.threshold, 'signal'] = -1
        df.loc[df['zscore'] < -self.threshold, 'signal'] = 1

        print("[ZScoreStrategy] signal counts:\n", df['signal'].value_counts())

        return df
