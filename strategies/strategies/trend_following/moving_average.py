from strategies.base import Strategy
import pandas as pd

class MovingAverageCrossover(Strategy):
    def __init__(self, short_window=50, long_window=200):
        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()
        df['short_ma'] = df['Close'].rolling(window=self.short_window).mean()
        df['long_ma'] = df['Close'].rolling(window=self.long_window).mean()
        df['signal'] = 0
        df.loc[df['short_ma'] > df['long_ma'], 'signal'] = 1
        df.loc[df['short_ma'] < df['long_ma'], 'signal'] = -1
        return df
