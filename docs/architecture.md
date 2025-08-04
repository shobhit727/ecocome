# Technical Architecture

## System Overview

The Stock Market Trading System is built using FastAPI and implements a real-time trading platform with simulated market activity. The system is designed to be modular, scalable, and maintainable.

## Core Components

### 1. API Layer (`api/`)

#### WebSocket Management (`websocket.py`)
- Manages real-time connections with clients
- Broadcasts market updates
- Handles client connections/disconnections

#### REST Endpoints (`endpoints.py`)
- Company registration and management
- Trader account operations
- Order placement and management
- Market data retrieval

### 2. Market Core (`market/`)

#### Order Matching (`matching.py`)
- Price-time priority matching algorithm
- Trade execution logic
- Portfolio updates

#### Fee Calculator (`fees.py`)
- Calculates trading fees
- Handles fee distribution
- Supports configurable fee structures

#### Market Simulation (`simulation.py`)
- Simulates price movements
- Processes pending orders
- Broadcasts market updates

### 3. Data Management (`data/`)

#### Data Storage (`storage.py`)
- In-memory data structures
- Thread-safe operations
- Central state management

#### Data Initialization (`initialization.py`)
- Sample data loading
- System initialization
- Test data setup

### 4. Models (`models.py`)
- Company model
- Trader model
- Order model
- Trade model

## Data Flow

1. **Market Simulation**
   ```
   simulation.py -> update prices
                -> match_orders()
                -> broadcast updates
   ```

2. **Order Processing**
   ```
   endpoints.py -> receive order
                -> add to order book
                -> match_orders()
                -> execute_trade()
                -> update portfolios
                -> broadcast trade
   ```

3. **WebSocket Updates**
   ```
   simulation.py -> market update
                -> websocket.py
                -> all connected clients
   ```

## Concurrency Management

- Uses `asyncio.Lock` for thread-safe operations
- Async/await patterns throughout
- WebSocket connection management

## Configuration

All system parameters are centralized in `config.py`:
- Trading fees
- Price simulation parameters
- API settings
- Sample data configuration

## Performance Considerations

1. **Data Storage**
   - In-memory storage for fast access
   - Lock-based concurrency control
   - Efficient data structures

2. **Order Matching**
   - Optimized sorting for price matching
   - Immediate execution when possible
   - Efficient order book updates

3. **WebSocket Broadcasting**
   - Asynchronous message dispatch
   - Connection management
   - Error handling
