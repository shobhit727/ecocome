from fastapi import FastAPI
import asyncio
from data import storage
from market import simulation
from api import endpoints, websocket
from config import settings

app = FastAPI()

# Include API routers
app.include_router(endpoints.router)

# Add WebSocket endpoint
app.websocket("/ws")(websocket.websocket_endpoint)


@app.on_event("startup")
async def startup_event():
    """Initialize application"""
    # Initialize data storage
    storage.data_store.initialize_sample_data()

    # Start market simulation
    asyncio.create_task(simulation.market_simulator())


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=settings.HOST, port=settings.PORT, reload=True)
