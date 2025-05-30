import pandas as pd

class Backtester:
    def __init__(self, starting_capital=10000):
        self.starting_capital = starting_capital

    def run(self, signals: pd.DataFrame) -> pd.DataFrame:
        df = signals.copy()
        df['position'] = df['signal'].shift(1).fillna(0)
        df['returns'] = df['Close'].pct_change().fillna(0)
        df['strategy_returns'] = df['position'] * df['returns']
        df['equity'] = (1 + df['strategy_returns']).cumprod() * self.starting_capital
        return df
