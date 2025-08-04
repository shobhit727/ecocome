# =====================
# IMPORTS
# =====================# =====================
# WEBSOCKET MANAGER
# =====================
from fastapi.websockets import WebSocketDisconnect

class ConnectionManager:
    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket) import FastAPI, HTTPException, WebSocket, status
from pydantic import BaseModel
import random
import asyncio
import uuid
from typing import Dict, List
from datetime import datetime


# =====================
# DATA MODELS
# =====================
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
    order_type: str


class Trade(BaseModel):
    trade_id: str
    symbol: str
    price: float
    quantity: int
    buyer: str
    seller: str
    timestamp: datetime


# =====================
# GLOBAL STATE
# =====================
app = FastAPI()

# Data stores
companies: Dict[str, Company] = {}
traders: Dict[str, Trader] = {}
order_book: Dict[str, Dict[str, List[Order]]] = {}
trade_history: List[Trade] = []
lock = asyncio.Lock()


# =====================
# WEBSOCKET MANAGER
# =====================
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


# =====================
# MARKET SIMULATION
# =====================
async def market_simulator():
    """Background task to simulate market activity"""
    while True:
        async with lock:
            # Update stock prices
            for symbol, company in companies.items():
                change = random.uniform(-1.5, 1.5)
                new_price = max(1, company.price * (1 + change / 100))
                companies[symbol].price = round(new_price, 2)

            # Process orders
            await match_orders()

            # Broadcast market update
            market_data = {
                "type": "market_update",
                "companies": {sym: comp.dict() for sym, comp in companies.items()},
                "timestamp": datetime.now().isoformat(),
            }
            await manager.broadcast(str(market_data))

        await asyncio.sleep(5)


async def match_orders():
    """Match buy and sell orders in the order book"""
    for symbol in list(order_book.keys()):
        if symbol not in order_book:
            continue

        # Sort orders by price priority
        buy_orders = sorted(
            [o for o in order_book[symbol].get("buy", []) if o.quantity > 0],
            key=lambda x: x.price,
            reverse=True,
        )
        sell_orders = sorted(
            [o for o in order_book[symbol].get("sell", []) if o.quantity > 0],
            key=lambda x: x.price,
        )

        # Execute matching orders
        while buy_orders and sell_orders:
            best_buy = buy_orders[0]
            best_sell = sell_orders[0]

            if best_buy.price >= best_sell.price:
                # Calculate trade parameters
                trade_price = round((best_buy.price + best_sell.price) / 2, 2)
                trade_quantity = min(best_buy.quantity, best_sell.quantity)

                # Execute trade
                await execute_trade(
                    buyer_id=best_buy.trader_id,
                    seller_id=best_sell.trader_id,
                    symbol=symbol,
                    price=trade_price,
                    quantity=trade_quantity,
                )

                # Update order quantities
                best_buy.quantity -= trade_quantity
                best_sell.quantity -= trade_quantity

                # Remove filled orders
                if best_buy.quantity <= 0:
                    buy_orders.pop(0)
                if best_sell.quantity <= 0:
                    sell_orders.pop(0)
            else:
                break

        # Update order book
        order_book[symbol]["buy"] = [o for o in buy_orders if o.quantity > 0]
        order_book[symbol]["sell"] = [o for o in sell_orders if o.quantity > 0]


async def execute_trade(
    buyer_id: str, seller_id: str, symbol: str, price: float, quantity: int
):
    """Execute a trade between buyer and seller"""
    # Update buyer portfolio
    buyer = traders[buyer_id]
    buyer.portfolio[symbol] = buyer.portfolio.get(symbol, 0) + quantity
    buyer.cash -= price * quantity

    # Update seller portfolio
    seller = traders[seller_id]
    seller.portfolio[symbol] = seller.portfolio.get(symbol, 0) - quantity
    seller.cash += price * quantity

    # Record trade
    trade = Trade(
        trade_id=str(uuid.uuid4()),
        symbol=symbol,
        price=price,
        quantity=quantity,
        buyer=buyer_id,
        seller=seller_id,
        timestamp=datetime.now(),
    )
    trade_history.append(trade)

    # Broadcast trade notification
    await manager.broadcast(str({"type": "trade_executed", "trade": trade.dict()}))


# =====================
# API ENDPOINTS: COMPANY
# =====================
@app.post("/company/register", response_model=Company)
async def register_company(name: str, symbol: str, initial_price: float, shares: int):
    """Register a new company and issue stock"""
    async with lock:
        if symbol in companies:
            raise HTTPException(
                status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
                detail="Company already exists",
            )

        company = Company(
            name=name,
            symbol=symbol,
            price=initial_price,
            outstanding_shares=shares,
            ipo_price=initial_price,
        )
        companies[symbol] = company
        order_book[symbol] = {"buy": [], "sell": []}

    return company


@app.get("/market/companies", response_model=Dict[str, Company])
async def get_companies():
    """Get all registered companies"""
    return companies


# =====================
# API ENDPOINTS: TRADER
# =====================
@app.post("/trader/register", response_model=Trader)
async def register_trader(name: str, cash: float):
    """Register a new trader"""
    trader_id = str(uuid.uuid4())
    trader = Trader(name=name, cash=cash)
    traders[trader_id] = trader
    return {"trader_id": trader_id, **trader.dict()}


@app.get("/trader/{trader_id}", response_model=Trader)
async def get_trader(trader_id: str):
    """Get trader portfolio"""
    if trader_id not in traders:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Trader not found"
        )
    return traders[trader_id]


# =====================
# API ENDPOINTS: TRADING
# =====================
@app.post("/market/order", status_code=status.HTTP_200_OK)
async def place_order(order: Order):
    """Place a buy or sell order"""
    async with lock:
        # Validate request
        if order.symbol not in companies:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Invalid stock symbol"
            )
        if order.trader_id not in traders:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Invalid trader ID"
            )
        if order.order_type not in ["buy", "sell"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid order type"
            )

        # Check trader resources
        trader = traders[order.trader_id]
        if order.order_type == "buy" and trader.cash < order.price * order.quantity:
            raise HTTPException(
                status_code=status.HTTP_201_CREATED, detail="Insufficient funds"
            )
        if order.order_type == "sell":
            current_shares = trader.portfolio.get(order.symbol, 0)
            if current_shares < order.quantity:
                raise HTTPException(
                    status_code=status.HTTP_202_ACCEPTED, detail="Insufficient shares"
                )

        # Add order to order book
        order_book[order.symbol][order.order_type].append(order)

        # Broadcast order book update
        await manager.broadcast(
            str(
                {
                    "type": "order_book_update",
                    "symbol": order.symbol,
                    "order_book": {
                        "buy": [o.dict() for o in order_book[order.symbol]["buy"]],
                        "sell": [o.dict() for o in order_book[order.symbol]["sell"]],
                    },
                }
            )
        )

    return {"message": "Order placed successfully"}


@app.get("/market/orderbook/{symbol}", response_model=Dict[str, List[Order]])
async def get_orderbook(symbol: str):
    """Get order book for a stock"""
    if symbol not in order_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid stock symbol"
        )
    return order_book[symbol]


@app.get("/market/trades", response_model=List[Trade])
async def get_trades(limit: int = 50):
    """Get recent trades"""
    return trade_history[-limit:]


@app.get("/market/price/{symbol}", response_model=float)
async def get_current_price(symbol: str):
    """Get current stock price"""
    if symbol not in companies:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid stock symbol"
        )
    return companies[symbol].price


# =====================
# WEBSOCKET ENDPOINT
# =====================
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket for real-time market updates"""
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except:
        manager.disconnect(websocket)


# =====================
# INITIALIZATION
# =====================
async def init_sample_data():
    """Initialize sample market data"""
    async with lock:
        # Sample company
        companies["AAPL"] = Company(
            name="Apple Inc.",
            symbol="AAPL",
            price=180.0,
            outstanding_shares=1000000,
            ipo_price=180.0,
        )
        order_book["AAPL"] = {"buy": [], "sell": []}

        # Sample traders
        trader1_id = str(uuid.uuid4())
        traders[trader1_id] = Trader(name="John Doe", cash=100000.0)

        trader2_id = str(uuid.uuid4())
        traders[trader2_id] = Trader(
            name="Jane Smith", cash=150000.0, portfolio={"AAPL": 500}
        )


@app.on_event("startup")
async def startup_event():
    """Startup initialization"""
    await init_sample_data()
    asyncio.create_task(market_simulator())


# =====================
# MAIN ENTRY POINT
# =====================
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.2", port=8000)
