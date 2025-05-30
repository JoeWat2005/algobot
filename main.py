from market.data_loader import Market
from strategies.moving_average import MovingAverageCrossoverStrategy
from backtester.simulator import Backtester

market = Market()
data = market.get_all_data()

strategy = MovingAverageCrossoverStrategy()
backtester = Backtester()

for ticker, df in data.items():
    signals = strategy.generate_signals(df)
    results = backtester.run(signals)
    print(f"{ticker} Final Equity: ${results['equity'].iloc[-1]:,.2f}")
