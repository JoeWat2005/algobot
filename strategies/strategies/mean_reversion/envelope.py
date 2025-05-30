from strategies.base import Strategy
import pandas as pd

class EnvelopeChannelStrategy(Strategy):
    def __init__(self, window=20, percentage=0.025):
        self.window = window
        self.percentage = percentage

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()
        df['ma'] = df['Close'].rolling(self.window).mean()
        df['upper_envelope'] = df['ma'] * (1 + self.percentage)
        df['lower_envelope'] = df['ma'] * (1 - self.percentage)
        df['signal'] = 0
        df.loc[df['Close'] > df['upper_envelope'], 'signal'] = -1
        df.loc[df['Close'] < df['lower_envelope'], 'signal'] = 1
        return df
