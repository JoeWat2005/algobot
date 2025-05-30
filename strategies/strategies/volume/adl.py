from strategies.base import Strategy
import pandas as pd

class AccumulationDistributionStrategy(Strategy):
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()
        clv = ((df['Close'] - df['Low']) - (df['High'] - df['Close'])) / (df['High'] - df['Low'])
        adl = (clv * df['Volume']).cumsum()
        df['adl'] = adl
        df['adl_ema'] = df['adl'].ewm(span=20).mean()
        df['signal'] = 0
        df.loc[df['adl'] > df['adl_ema'], 'signal'] = 1
        df.loc[df['adl'] < df['adl_ema'], 'signal'] = -1
        return df
