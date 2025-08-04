# market/simulation.py
import random
import asyncio
from datetime import datetime
from ..data import storage
from ..config import settings
from .matching import match_orders
from ..api.websocket import manager


async def market_simulator():
    """Background task to simulate market activity"""
    while True:
        async with storage.data_store.lock:
            # Update stock prices
            for symbol, company in storage.data_store.companies.items():
                min_change, max_change = settings.PRICE_FLUCTUATION_RANGE
                change = random.uniform(min_change, max_change)
                new_price = max(1, company["price"] * (1 + change / 100))
                storage.data_store.companies[symbol]["price"] = round(new_price, 2)

            # Process orders
            await match_orders()

            # Broadcast market update
            market_data = {
                "type": "market_update",
                "companies": storage.data_store.companies,
                "timestamp": datetime.now().isoformat(),
            }
            await manager.broadcast(str(market_data))

        await asyncio.sleep(settings.MARKET_UPDATE_INTERVAL)
