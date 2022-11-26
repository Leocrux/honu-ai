from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from fastapi import FastAPI

from app.api import hello
from app.settings import MONGO_DB_URL, MONGO_DB
from app.models import __beanie_models__

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    mongodb_client = AsyncIOMotorClient(MONGO_DB_URL)
    await init_beanie(mongodb_client[MONGO_DB], document_models=__beanie_models__)
    app.include_router(hello.router)


@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()
