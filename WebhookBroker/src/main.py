from fastapi import FastAPI
from infrastructure.api.RouterManager import RouterManager
from config.Logger_config import get_logger

app = FastAPI()
logger = get_logger("uvicorn")

RouterManager.create_routes(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
