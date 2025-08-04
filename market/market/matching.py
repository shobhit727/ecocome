# market/matching.py
import uuid
from datetime import datetime
from ..models import Trade
from ..data import storage
from .fees import calculate_trading_fees


async def execute_trade(
    buyer_id: str, seller_id: str, symbol: str, price: float, quantity: int
):
    """Execute a trade between buyer and seller with fees"""
    async with storage.data_store.lock:
        # Get references to traders
        buyer = storage.data_store.traders[buyer_id]
        seller = storage.data_store.traders[seller_id]

        # Calculate trade value and fees
        trade_value = price * quantity
        fees = calculate_trading_fees(trade_value)

        # Update buyer portfolio (pay price + fees)
        buyer["portfolio"][symbol] = buyer["portfolio"].get(symbol, 0) + quantity
        buyer["cash"] -= trade_value + fees["buyer_fee"]

        # Update seller portfolio (receive price - fees)
        seller["portfolio"][symbol] = seller["portfolio"].get(symbol, 0) - quantity
        seller["cash"] += trade_value - fees["seller_fee"]

        # Record trade
        trade = Trade(
            trade_id=str(uuid.uuid4()),
            symbol=symbol,
            price=price,
            quantity=quantity,
            buyer=buyer_id,
            seller=seller_id,
            fees=fees,
            timestamp=datetime.now(),
        )
        storage.data_store.trade_history.append(trade)

        return trade


async def match_orders():
    """Match buy and sell orders in the order book"""
    data_store = storage.data_store
    for symbol in list(data_store.order_book.keys()):
        if symbol not in data_store.order_book:
            continue

        # Sort orders by price priority
        buy_orders = sorted(
            [o for o in data_store.order_book[symbol].get("buy", []) if o.quantity > 0],
            key=lambda x: x.price,
            reverse=True,
        )
        sell_orders = sorted(
            [
                o
                for o in data_store.order_book[symbol].get("sell", [])
                if o.quantity > 0
            ],
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
        data_store.order_book[symbol]["buy"] = [o for o in buy_orders if o.quantity > 0]
        data_store.order_book[symbol]["sell"] = [
            o for o in sell_orders if o.quantity > 0
        ]
