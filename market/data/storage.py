# ==============================================
# Market Data Storage System
# ==============================================
# Central data storage for the trading system:
# - Companies: Stores registered companies and their stocks
# - Traders: Manages trader accounts and portfolios
# - Order Book: Tracks all pending buy/sell orders
# - Trade History: Records all executed trades
#
# Uses asyncio.Lock for thread-safe operations
# ==============================================

import asyncio
from models import Company, Trader, Order, Trade
from config import settings


class DataStorage:
    def __init__(self):
        self.companies = {}
        self.traders = {}
        self.order_book = {}
        self.trade_history = []
        self.lock = asyncio.Lock()

    def initialize_sample_data(self):
        from data.initialization import init_sample_data

        init_sample_data(self)


# Global data store instance
data_store = DataStorage()
