# Stock Market Trading System - AI Agent Instructions

## Project Overview
This is a FastAPI-based stock market trading simulation system with real-time updates via WebSocket. The system simulates market activity, handles trading operations, and maintains a synchronized state across all components.

## Architecture

### Core Components
- `main.py`: Entry point, FastAPI setup, and background task initialization
- `api/`: REST endpoints and WebSocket handling
- `data/`: Data storage and initialization
- `market/`: Core market logic (matching, fees, simulation)
- `models.py`: Pydantic models for data validation

### Data Flow
1. Market simulation (`market/simulation.py`) updates prices every 5 seconds
2. Trading operations are processed through REST endpoints (`api/endpoints.py`)
3. Order matching (`market/matching.py`) executes trades when conditions match
4. Real-time updates broadcast via WebSocket (`api/websocket.py`)

## Key Patterns

### Concurrency Management
- Use `asyncio.Lock` for thread-safe data access:
```python
async with storage.data_store.lock:
    # Perform atomic operations here
```

### WebSocket Broadcasting
- Use `manager.broadcast()` to send updates to all connected clients
- Market updates are automatically broadcast after price changes

### Price Simulation
- Prices fluctuate within `PRICE_FLUCTUATION_RANGE` (-1.5% to +1.5%)
- Updates occur every `MARKET_UPDATE_INTERVAL` (5 seconds)

### Trading Fee Structure
- Fixed percentage fee (0.1%) applied to trade value
- Both buyer and seller pay equal fees
- See `market/fees.py` for fee calculation logic

## Development Workflow

### Running the Application
```bash
# Start the FastAPI server
python market/main.py
```
Server runs on `127.0.0.2:8000` by default (configured in `config.py`)

### Testing Routes
- REST API: `http://127.0.0.2:8000/docs` (Swagger UI)
- WebSocket: `ws://127.0.0.2:8000/ws`

### State Management
- All state is held in `DataStorage` instance (`data/storage.py`)
- Use lock when modifying shared state
- Sample data initialized on startup from `config.py`

## Common Tasks

### Adding New Trading Features
1. Update models in `models.py`
2. Add endpoints in `api/endpoints.py`
3. Implement business logic in `market/` modules
4. Update WebSocket broadcasts if real-time updates needed

### Modifying Market Behavior
- Adjust simulation parameters in `config.py`
- Modify price movement logic in `market/simulation.py`
- Update order matching rules in `market/matching.py`
