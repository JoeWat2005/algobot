from strategies.base import Strategy
import pandas as pd

class MLStubStrategy(Strategy):
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()
        df['signal'] = 0  # Placeholder for future ML logic
        return df
