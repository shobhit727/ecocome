# Stock Market Trading System

A real-time trading platform with price simulation and WebSocket updates built with FastAPI.

## Features

- Real-time market simulation with price fluctuations
- Live order matching and trade execution
- WebSocket-based real-time market updates
- Trading fee calculation and management
- RESTful API for market operations
- Comprehensive test suite

## System Architecture

### Core Components

- **API Layer** (`api/`)
  - REST endpoints for trading operations
  - WebSocket handling for real-time updates
  
- **Market Core** (`market/`)
  - Order matching engine
  - Trading fee calculation
  - Market price simulation
  
- **Data Management** (`data/`)
  - In-memory data storage
  - Sample data initialization
  
- **Models** (`models.py`)
  - Data models for companies, traders, orders, and trades

## Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

1. Clone the repository:
```bash
git clone https://github.com/shobhit727/ecocome.git
cd ecocome
```

2. Install dependencies:
```bash
pip install -e .
```

### Running the Application

1. Start the server:
```bash
python market/main.py
```

The server will start on `http://127.0.0.2:8000`

### API Documentation

Once running, visit:
- Swagger UI: `http://127.0.0.2:8000/docs`
- ReDoc: `http://127.0.0.2:8000/redoc`

## Key Features

### Real-time Market Simulation

- Prices update every 5 seconds
- Random fluctuations within -1.5% to +1.5%
- WebSocket broadcasts of market updates

### Order Matching

- Price-time priority matching
- Immediate execution when prices match
- Support for both buy and sell orders

### Trading Fees

- Fixed percentage fee (0.1%)
- Applied to both buyer and seller
- Automatically calculated and deducted

### Portfolio Management

- Real-time portfolio updates
- Cash balance tracking
- Position tracking for all traders

## Testing

Run the test suite:
```bash
pytest tests/
```

### Test Coverage

- Integration tests for market operations
- WebSocket connection testing
- Order matching verification
- Fee calculation validation

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
