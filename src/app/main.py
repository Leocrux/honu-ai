from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from fastapi import FastAPI

from app.settings import MONGO_DB_URL, MONGO_DB
from app.models import ServiceProviderModel
from app.api import router as ServiceProviderRouter

app = FastAPI()


@app.get("/", tags=["Root"])
def hello():
    return {"Hello": "World"}


@app.on_event("startup")
async def startup_event():
    mongodb_client = AsyncIOMotorClient(MONGO_DB_URL)
    await init_beanie(mongodb_client[MONGO_DB], document_models=[ServiceProviderModel])
    app.include_router(ServiceProviderRouter, tags=["ServiceProvider"], prefix="/service_provider")
