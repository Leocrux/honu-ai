from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from fastapi import FastAPI

from app.settings import MONGO_DB_URL, MONGO_DB
from app.models import ServiceProviderSchema
from app.api import router as ServiceProviderRouter

app = FastAPI()


@app.get("/", tags=["Root"])
def hello():
    return {"Hello": "World"}


@app.on_event("startup")
async def startup_event():
    app.mongodb_client = AsyncIOMotorClient(MONGO_DB_URL)
    app.mongodb = app.mongodb_client[MONGO_DB]
    # await init_beanie(mongodb_client[MONGO_DB], document_models=[ServiceProviderSchema])
    app.include_router(ServiceProviderRouter, tags=["ServiceProvider"], prefix="/service_provider")


@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()
