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
