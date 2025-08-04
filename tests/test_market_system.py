# ==============================================
# Market System Test Configuration
# ==============================================
import pytest
from fastapi.testclient import TestClient
from market.main import app
import json

client = TestClient(app)


def test_get_companies():
    """Test retrieving list of companies"""
    response = client.get("/market/companies")
    assert response.status_code == 200
    companies = response.json()
    assert "AAPL" in companies
    print("Companies test passed:", json.dumps(companies, indent=2))


def test_register_trader():
    """Test trader registration"""
    response = client.post(
        "/trader/register", params={"name": "Test Trader", "cash": 50000.0}
    )
    assert response.status_code == 200
    trader = response.json()
    assert trader["name"] == "Test Trader"
    assert trader["cash"] == 50000.0
    assert "trader_id" in trader
    print("Trader registration test passed:", json.dumps(trader, indent=2))
    return trader["trader_id"]


def test_place_order(trader_id):
    """Test placing a market order"""
    buy_order = {
        "trader_id": trader_id,
        "symbol": "AAPL",
        "price": 180.0,
        "quantity": 10,
        "order_type": "buy",
    }
    response = client.post("/market/order", json=buy_order)
    assert response.status_code == 200
    print("Order placement test passed:", response.json())


def test_get_orderbook():
    """Test retrieving the order book"""
    response = client.get("/market/orderbook/AAPL")
    assert response.status_code == 200
    order_book = response.json()
    assert "buy" in order_book
    assert "sell" in order_book
    print("Order book test passed:", json.dumps(order_book, indent=2))


def test_get_market_price():
    """Test getting current market price"""
    response = client.get("/market/price/AAPL")
    assert response.status_code == 200
    price = response.json()
    assert isinstance(price, float)
    assert price > 0
    print("Market price test passed. AAPL price:", price)


def test_estimate_fees():
    """Test fee calculation"""
    response = client.get(
        "/market/fee-estimate", params={"price": 180.0, "quantity": 10}
    )
    assert response.status_code == 200
    fees = response.json()
    assert "trade_value" in fees
    assert "fees" in fees
    assert "buyer_total" in fees
    assert "seller_receives" in fees
    print("Fee estimation test passed:", json.dumps(fees, indent=2))


def run_all_tests():
    """Run all market system tests"""
    print("\n=== Starting Market System Tests ===\n")

    test_get_companies()
    trader_id = test_register_trader()
    test_place_order(trader_id)
    test_get_orderbook()
    test_get_market_price()
    test_estimate_fees()

    print("\n=== All Tests Passed Successfully ===\n")


if __name__ == "__main__":
    run_all_tests()
