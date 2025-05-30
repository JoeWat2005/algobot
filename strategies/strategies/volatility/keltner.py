from strategies.base import Strategy
import pandas as pd

class KeltnerChannelStrategy(Strategy):
    def __init__(self, period=20, atr_multiplier=2):
        self.period = period
        self.atr_multiplier = atr_multiplier

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()
        df['typical_price'] = (df['High'] + df['Low'] + df['Close']) / 3
        df['ma'] = df['typical_price'].rolling(self.period).mean()
        tr1 = df['High'] - df['Low']
        tr2 = abs(df['High'] - df['Close'].shift())
        tr3 = abs(df['Low'] - df['Close'].shift())
        df['tr'] = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        df['atr'] = df['tr'].rolling(self.period).mean()
        df['upper_band'] = df['ma'] + self.atr_multiplier * df['atr']
        df['lower_band'] = df['ma'] - self.atr_multiplier * df['atr']
        df['signal'] = 0
        df.loc[df['Close'] > df['upper_band'], 'signal'] = -1
        df.loc[df['Close'] < df['lower_band'], 'signal'] = 1
        return df