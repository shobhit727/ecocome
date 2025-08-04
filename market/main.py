# ==============================================
# Stock Market Trading System
# ==============================================
# This is the main entry point for the trading application.
# It sets up the FastAPI server, initializes data storage,
# and starts the market simulation.
# ==============================================

from fastapi import FastAPI
import asyncio
from data import storage
from market import simulation
from api import endpoints, websocket
from config import settings

# Initialize FastAPI application
app = FastAPI(
    title="Stock Market Trading System",
    description="A real-time trading platform with price simulation and WebSocket updates",
    version="1.0.0",
)

# Register API endpoints from the endpoints module
app.include_router(endpoints.router)

# Set up WebSocket endpoint for real-time market updates
app.websocket("/ws")(websocket.websocket_endpoint)


@app.on_event("startup")
async def startup_event():
    """
    Initialize the trading application on startup.
    This function:
    1. Loads sample companies and traders into the data store
    2. Starts the market simulation in the background
       - Simulates price movements
       - Processes pending orders
       - Broadcasts market updates via WebSocket
    """
    # Initialize data storage with sample companies and traders
    storage.data_store.initialize_sample_data()

    # Start market simulation as a background task
    # This continuously updates prices and processes orders
    asyncio.create_task(simulation.market_simulator())


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=settings.HOST, port=settings.PORT, reload=True)
