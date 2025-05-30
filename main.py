from market.data_loader import Market
from strategies.moving_average import *

from market.data_loader import Market

market = Market()
all_data = market.get_all_data()

for ticker, df in all_data.items():
    print(f"{ticker}: {df.shape}")
