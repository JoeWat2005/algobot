from strategies.base import Strategy
import pandas as pd

class PatternRecognizerStrategy(Strategy):
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()
        df['signal'] = 0
        df['candle'] = df['Close'] - df['Open']
        df.loc[(df['candle'] > 0) & (df['candle'].shift() < 0), 'signal'] = 1  # Bullish reversal
        df.loc[(df['candle'] < 0) & (df['candle'].shift() > 0), 'signal'] = -1 # Bearish reversal
        return df