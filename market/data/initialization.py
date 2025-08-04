import uuid
from config import settings
from models import Company, Trader


def init_sample_data(storage):
    # Create sample companies
    for company_data in settings.SAMPLE_COMPANIES:
        storage.companies[company_data["symbol"]] = Company(
            name=company_data["name"],
            symbol=company_data["symbol"],
            price=company_data["price"],
            outstanding_shares=company_data["outstanding_shares"],
            ipo_price=company_data["ipo_price"],
        )
        storage.order_book[company_data["symbol"]] = {"buy": [], "sell": []}

    # Create sample traders
    for trader_data in settings.SAMPLE_TRADERS:
        trader_id = str(uuid.uuid4())
        storage.traders[trader_id] = Trader(
            name=trader_data["name"],
            cash=trader_data["cash"],
            portfolio=trader_data.get("portfolio", {}),
        )
