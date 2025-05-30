from strategies.base import Strategy
import pandas as pd

class IchimokuCloudStrategy(Strategy):
    def __init__(self):
        self.tenkan_window = 9
        self.kijun_window = 26
        self.senkou_span_b_window = 52

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()

        high_9 = df['High'].rolling(window=self.tenkan_window).max()
        low_9 = df['Low'].rolling(window=self.tenkan_window).min()
        df['tenkan_sen'] = (high_9 + low_9) / 2

        high_26 = df['High'].rolling(window=self.kijun_window).max()
        low_26 = df['Low'].rolling(window=self.kijun_window).min()
        df['kijun_sen'] = (high_26 + low_26) / 2

        df['senkou_span_a'] = ((df['tenkan_sen'] + df['kijun_sen']) / 2).shift(self.kijun_window)

        high_52 = df['High'].rolling(window=self.senkou_span_b_window).max()
        low_52 = df['Low'].rolling(window=self.senkou_span_b_window).min()
        df['senkou_span_b'] = ((high_52 + low_52) / 2).shift(self.kijun_window)

        df['signal'] = 0
        df.loc[df['Close'] > df['senkou_span_a'], 'signal'] = 1
        df.loc[df['Close'] < df['senkou_span_b'], 'signal'] = -1

        return df
