from strategies.base import Strategy
import pandas as pd

class ChaikinMoneyFlowStrategy(Strategy):
    def __init__(self, period=20):
        self.period = period

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()
        mf_multiplier = ((df['Close'] - df['Low']) - (df['High'] - df['Close'])) / (df['High'] - df['Low'])
        mf_volume = mf_multiplier * df['Volume']
        df['cmf'] = mf_volume.rolling(self.period).sum() / df['Volume'].rolling(self.period).sum()
        df['signal'] = 0
        df.loc[df['cmf'] > 0, 'signal'] = 1
        df.loc[df['cmf'] < 0, 'signal'] = -1
        return df
