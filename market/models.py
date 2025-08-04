# ==============================================
# Market Data Models
# ==============================================
# This module defines the core data models for the trading system:
# - Company: Represents listed companies and their stock details
# - Trader: Represents market participants and their portfolios
# - Order: Represents buy/sell orders in the market
# - Trade: Represents executed trades between buyers and sellers
# ==============================================

from pydantic import BaseModel
from datetime import datetime
from typing import Dict, List, Optional


class Company(BaseModel):
    name: str
    symbol: str
    price: float
    outstanding_shares: int
    ipo_price: float


class Trader(BaseModel):
    name: str
    cash: float
    portfolio: Dict[str, int] = {}


class Order(BaseModel):
    trader_id: str
    symbol: str
    price: float
    quantity: int
    order_type: str  # 'buy' or 'sell'


class Trade(BaseModel):
    trade_id: str
    symbol: str
    price: float
    quantity: int
    buyer: str
    seller: str
    fees: Dict[str, float]  # {'buyer_fee': 1.5, 'seller_fee': 1.5}
    timestamp: datetime
