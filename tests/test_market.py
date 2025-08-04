import asyncio
import websockets
import httpx
import json
import pytest
from fastapi.testclient import TestClient
from market.main import app
import uvicorn
import threading
import time
from contextlib import contextmanager


@contextmanager
def run_server():
    """Start server in a separate thread"""
    server = uvicorn.Server(config=uvicorn.Config(app, host="127.0.0.2", port=8000))
    thread = threading.Thread(target=server.run)
    thread.daemon = True
    thread.start()
    time.sleep(2)  # Wait for server to start
    try:
        yield
    finally:
        server.should_exit = True


async def test_market_system():
    """Test the complete market system flow"""
    with run_server():
        async with httpx.AsyncClient(base_url="http://127.0.0.2:8000") as client:
            # 1. Test getting companies
            response = await client.get("/market/companies")
        assert response.status_code == 200
        companies = response.json()
        print("Companies in market:", json.dumps(companies, indent=2))

        # 2. Register a new trader
        response = await client.post(
            "/trader/register", params={"name": "Test Trader", "cash": 50000.0}
        )
        assert response.status_code == 200
        trader = response.json()
        trader_id = trader["trader_id"]
        print("Registered trader:", json.dumps(trader, indent=2))

        # 3. Place a buy order
        buy_order = {
            "trader_id": trader_id,
            "symbol": "AAPL",
            "price": 180.0,
            "quantity": 10,
            "order_type": "buy",
        }
        response = await client.post("/market/order", json=buy_order)
        assert response.status_code == 200
        print("Buy order placed:", response.json())

        # Wait for order processing
        await asyncio.sleep(2)

        # Get trader's updated portfolio
        response = await client.get(f"/trader/{trader_id}")
        assert response.status_code == 200
        updated_trader = response.json()
        print("Updated trader portfolio:", json.dumps(updated_trader, indent=2))

        # 4. Get order book
        response = await client.get("/market/orderbook/AAPL")
        assert response.status_code == 200
        order_book = response.json()
        print("Order book for AAPL:", json.dumps(order_book, indent=2))

        # 5. Test WebSocket connection
        async with websockets.connect("ws://127.0.0.2:8000/ws") as websocket:
            print("Connected to WebSocket")
            # Wait for market update
            message = await websocket.recv()
            market_update = json.loads(message.replace("'", '"'))
            print("Received market update:", json.dumps(market_update, indent=2))


if __name__ == "__main__":
    asyncio.run(test_market_system())
