# ==============================================
# Market Configuration
# ==============================================
# Central configuration for the trading system:
#
# Trading Settings:
# - Trading fees and fee structure
# - Market simulation parameters
# - Price fluctuation ranges
#
# System Settings:
# - API host and port
# - Update intervals
#
# Sample Data:
# - Initial companies and stocks
# - Sample trader accounts
# ==============================================


class Settings:
    # Trading fees (percentage of trade value)
    TRADING_FEE_PERCENT = 0.1  # 0.1% fee

    # Market simulation parameters
    PRICE_FLUCTUATION_RANGE = (-1.5, 1.5)  # Percentage
    MARKET_UPDATE_INTERVAL = 5  # Seconds

    # API settings
    HOST = "127.0.0.2"
    PORT = 8000

    # Initial sample data
    SAMPLE_COMPANIES = [
        {
            "name": "Apple Inc.",
            "symbol": "AAPL",
            "price": 180.0,
            "outstanding_shares": 1000000,
            "ipo_price": 180.0,
        }
    ]

    SAMPLE_TRADERS = [
        {"name": "John Doe", "cash": 100000.0, "portfolio": {}},
        {"name": "Jane Smith", "cash": 150000.0, "portfolio": {"AAPL": 500}},
    ]


settings = Settings()
