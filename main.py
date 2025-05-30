from market.data_loader import Market
from backtester.simulator import Backtester

market = Market()
data = market.get_all_data()

backtester = Backtester()

for ticker, df in data.items():
    print(f"\n=== Processing {ticker} ===")

    # Generate signals
    signals = strategy.generate_signals(df)

    # Run backtest
    results = backtester.run(signals)

    # Print final equity
    print(f"{ticker} Final Equity: ${results['equity'].iloc[-1]:,.2f}")

    # Print the last 100 rows of the fully processed DataFrame
    print(results[['Close', 'short_ma', 'long_ma', 'signal', 'position', 'strategy_returns', 'equity']].tail(100))
