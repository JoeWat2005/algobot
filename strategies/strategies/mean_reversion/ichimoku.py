from strategies.base import Strategy
import pandas as pd

class IchimokuCloudStrategy(Strategy):
    def __init__(self):
        self.tenkan_window = 9
        self.kijun_window = 26
        self.senkou_span_b_window = 52

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()
        df['tenkan_sen'] = (df['High'].rolling(self.tenkan_window).max() + df['Low'].rolling(self.tenkan_window).min()) / 2
        df['kijun_sen'] = (df['High'].rolling(self.kijun_window).max() + df['Low'].rolling(self.kijun_window).min()) / 2
        df['senkou_span_a'] = ((df['tenkan_sen'] + df['kijun_sen']) / 2).shift(self.kijun_window)
        df['senkou_span_b'] = ((df['High'].rolling(self.senkou_span_b_window).max() + df['Low'].rolling(self.senkou_span_b_window).min()) / 2).shift(self.kijun_window)
        df['signal'] = 0
        df.loc[df['Close'] > df['senkou_span_a'], 'signal'] = 1
        df.loc[df['Close'] < df['senkou_span_b'], 'signal'] = -1
        return df