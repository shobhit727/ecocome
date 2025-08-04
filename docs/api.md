# API Documentation

## REST Endpoints

### Company Management

#### Register Company
- **Endpoint**: `POST /company/register`
- **Parameters**:
  - `name`: Company name (string)
  - `symbol`: Trading symbol (string)
  - `initial_price`: Initial stock price (float)
  - `shares`: Outstanding shares (integer)
- **Response**: Company object

#### Get Companies
- **Endpoint**: `GET /market/companies`
- **Response**: Dictionary of companies with their details

### Trader Operations

#### Register Trader
- **Endpoint**: `POST /trader/register`
- **Parameters**:
  - `name`: Trader name (string)
  - `cash`: Initial cash balance (float)
- **Response**: Trader object with generated trader_id

#### Get Trader Details
- **Endpoint**: `GET /trader/{trader_id}`
- **Response**: Trader object with current portfolio and cash balance

### Trading Operations

#### Place Order
- **Endpoint**: `POST /market/order`
- **Body**:
  ```json
  {
    "trader_id": "string",
    "symbol": "string",
    "price": float,
    "quantity": int,
    "order_type": "buy" | "sell"
  }
  ```
- **Response**: Order confirmation

#### Get Order Book
- **Endpoint**: `GET /market/orderbook/{symbol}`
- **Response**: Current buy and sell orders for the symbol

#### Get Market Price
- **Endpoint**: `GET /market/price/{symbol}`
- **Response**: Current market price for the symbol

#### Estimate Trading Fees
- **Endpoint**: `GET /market/fee-estimate`
- **Parameters**:
  - `price`: Trade price (float)
  - `quantity`: Number of shares (integer)
- **Response**: Fee estimates for buyer and seller

## WebSocket API

### Market Updates
- **Endpoint**: `ws://127.0.0.2:8000/ws`
- **Events**:
  - Market price updates (every 5 seconds)
  - Trade execution notifications
  - Order book updates

### Message Format
```json
{
  "type": "market_update",
  "companies": {
    "AAPL": {
      "price": 180.0,
      "symbol": "AAPL",
      "name": "Apple Inc."
    }
  },
  "timestamp": "2025-08-05T12:00:00.000Z"
}
```
