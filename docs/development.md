# Development Guide

## Setup and Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Git

### Local Development Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/shobhit727/ecocome.git
   cd ecocome
   ```

2. **Install Dependencies**
   ```bash
   pip install -e .
   ```

3. **Run the Application**
   ```bash
   python market/main.py
   ```

## Project Structure

```
ecocome/
├── market/
│   ├── api/
│   │   ├── endpoints.py
│   │   └── websocket.py
│   ├── data/
│   │   ├── initialization.py
│   │   └── storage.py
│   ├── market/
│   │   ├── fees.py
│   │   ├── matching.py
│   │   └── simulation.py
│   ├── config.py
│   ├── main.py
│   └── models.py
├── tests/
│   ├── test_market.py
│   └── test_market_system.py
└── docs/
    ├── api.md
    └── architecture.md
```

## Development Guidelines

### Code Style
- Follow PEP 8
- Use type hints
- Write descriptive docstrings
- Keep functions focused and small

### Testing
1. **Running Tests**
   ```bash
   pytest tests/
   ```

2. **Test Coverage**
   ```bash
   pytest --cov=market tests/
   ```

### Adding New Features

1. **Adding a New Endpoint**
   - Add route to `api/endpoints.py`
   - Update API documentation
   - Add corresponding tests

2. **Modifying Market Behavior**
   - Update relevant files in `market/`
   - Adjust configuration in `config.py`
   - Test thoroughly

3. **Adding Models**
   - Define new models in `models.py`
   - Update documentation
   - Add validation tests

### WebSocket Development

1. **Broadcasting New Events**
   ```python
   await manager.broadcast(
       str({
           "type": "event_type",
           "data": event_data,
           "timestamp": datetime.now().isoformat()
       })
   )
   ```

2. **Adding New Message Types**
   - Document in API documentation
   - Update client handling code
   - Add test cases

## Common Development Tasks

### 1. Adding a New Company
```python
company = Company(
    name="New Corp",
    symbol="NEWC",
    price=100.0,
    outstanding_shares=1000000,
    ipo_price=100.0
)
```

### 2. Implementing a New Order Type
1. Update `models.py`
2. Modify matching logic
3. Update API endpoints
4. Add tests

### 3. Adding Trading Features
1. Plan the feature
2. Update relevant components
3. Add documentation
4. Write tests
5. Update API documentation

## Debugging

### Common Issues

1. **WebSocket Connections**
   - Check client connection status
   - Verify message format
   - Check error handling

2. **Order Matching**
   - Log order book state
   - Verify price comparisons
   - Check portfolio updates

3. **Market Simulation**
   - Monitor price changes
   - Verify update intervals
   - Check broadcast messages

### Logging

Use Python's logging module:
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Market update: %s", market_data)
logger.error("Order matching failed: %s", error)
```

## Deployment

### Production Setup
1. Use a production ASGI server
2. Configure environment variables
3. Set up monitoring
4. Configure logging

### Configuration
Update `config.py` for production:
```python
class ProductionSettings(Settings):
    HOST = "0.0.0.0"
    PORT = 80
    MARKET_UPDATE_INTERVAL = 5
    TRADING_FEE_PERCENT = 0.1
```
