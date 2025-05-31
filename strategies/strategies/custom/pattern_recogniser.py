from strategies.base import Strategy
import pandas as pd

class PatternRecognizerStrategy(Strategy):
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()

        # Flatten MultiIndex columns if present
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        print("\n[PatternRecognizerStrategy] Input index:", type(df.index))
        print("[PatternRecognizerStrategy] Input head:")
        print(df.head(3))

        # Candlestick pattern recognition
        df['signal'] = 0
        df['candle'] = df['Close'] - df['Open']
        prev_candle = df['candle'].shift().fillna(0)

        df.loc[(df['candle'] > 0) & (prev_candle < 0), 'signal'] = 1   # Bullish reversal
        df.loc[(df['candle'] < 0) & (prev_candle > 0), 'signal'] = -1  # Bearish reversal

        print("[PatternRecognizerStrategy] signal counts:\n", df['signal'].value_counts())

        return df
