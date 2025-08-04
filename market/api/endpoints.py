# api/endpoints.py
from fastapi import APIRouter, HTTPException, status
from ..models import Company, Trader, Order, Trade
from ..data import storage
from ..market.fees import calculate_trading_fees
import uuid

router = APIRouter()


# =====================
# COMPANY ENDPOINTS
# =====================
@router.post("/company/register", response_model=Company)
async def register_company(name: str, symbol: str, initial_price: float, shares: int):
    async with storage.data_store.lock:
        if symbol in storage.data_store.companies:
            raise HTTPException(
                status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
                detail="Company already exists",
            )

        company = {
            "name": name,
            "symbol": symbol,
            "price": initial_price,
            "outstanding_shares": shares,
            "ipo_price": initial_price,
        }
        storage.data_store.companies[symbol] = company
        storage.data_store.order_book[symbol] = {"buy": [], "sell": []}

    return company


@router.get("/market/companies", response_model=dict)
async def get_companies():
    return storage.data_store.companies


# =====================
# TRADER ENDPOINTS
# =====================
@router.post("/trader/register", response_model=Trader)
async def register_trader(name: str, cash: float):
    trader_id = str(uuid.uuid4())
    trader = {"name": name, "cash": cash, "portfolio": {}}
    storage.data_store.traders[trader_id] = trader
    return {"trader_id": trader_id, **trader}


@router.get("/trader/{trader_id}", response_model=Trader)
async def get_trader(trader_id: str):
    if trader_id not in storage.data_store.traders:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Trader not found"
        )
    return storage.data_store.traders[trader_id]


# =====================
# TRADING ENDPOINTS
# =====================
@router.post("/market/order", status_code=status.HTTP_200_OK)
async def place_order(order: Order):
    async with storage.data_store.lock:
        # Validate request
        if order.symbol not in storage.data_store.companies:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Invalid stock symbol"
            )
        if order.trader_id not in storage.data_store.traders:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Invalid trader ID"
            )
        if order.order_type not in ["buy", "sell"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid order type"
            )

        # Check trader resources
        trader = storage.data_store.traders[order.trader_id]
        if order.order_type == "buy":
            # Calculate potential fees (estimate)
            potential_fees = calculate_trading_fees(order.price * order.quantity)[
                "buyer_fee"
            ]
            total_cost = order.price * order.quantity + potential_fees

            if trader["cash"] < total_cost:
                raise HTTPException(
                    status_code=status.HTTP_201_CREATED, detail="Insufficient funds"
                )

        if order.order_type == "sell":
            current_shares = trader["portfolio"].get(order.symbol, 0)
            if current_shares < order.quantity:
                raise HTTPException(
                    status_code=status.HTTP_202_ACCEPTED, detail="Insufficient shares"
                )

        # Add order to order book
        storage.data_store.order_book[order.symbol][order.order_type].append(order)

    return {"message": "Order placed successfully"}


@router.get("/market/orderbook/{symbol}", response_model=dict)
async def get_orderbook(symbol: str):
    if symbol not in storage.data_store.order_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid stock symbol"
        )
    return storage.data_store.order_book[symbol]


@router.get("/market/trades", response_model=list)
async def get_trades(limit: int = 50):
    return storage.data_store.trade_history[-limit:]


@router.get("/market/price/{symbol}", response_model=float)
async def get_current_price(symbol: str):
    if symbol not in storage.data_store.companies:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid stock symbol"
        )
    return storage.data_store.companies[symbol]["price"]


@router.get("/market/fee-estimate", response_model=dict)
async def estimate_fee(price: float, quantity: int):
    """Estimate trading fees for a transaction"""
    trade_value = price * quantity
    fees = calculate_trading_fees(trade_value)
    return {
        "trade_value": trade_value,
        "fees": fees,
        "buyer_total": trade_value + fees["buyer_fee"],
        "seller_receives": trade_value - fees["seller_fee"],
    }
