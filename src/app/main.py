from typing import Union

from beanie import init_beanie
from fastapi import APIRouter, FastAPI, Query
from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorClient

from app.api import router as ServiceProviderRouter
from app.models import ServiceProviderModel
from app.settings import MONGO_DB, MONGO_DB_URL
from tests.datafile import testdata

router = APIRouter()

app = FastAPI()


@app.get("/", tags=["Root"])
def hello():
    return {"Hello": "World"}


# Task 3


@app.get(
    "/get_available_providers",
    response_description="Task3",
    response_model=list[ServiceProviderModel],
)
async def get_available_providers(
    skills: list[str] = Query(),
    budget: int = Query(),
    reviews__gte: Union[float, None] = Query(default=None),
):
    """
    Returns all current or past available providers that have **ALL** of the skills and one period that fits budget

    @todo filter maybe by future dates

    @todo If looking for skills [A, B] maybe can return 2 different providers with skills [A], [B] that
        match description and sum(budget) - requirements insufficient
    """
    aggr_pipeline = [
        {
            "$addFields": {
                "availability": {
                    "$map": {
                        "input": "$availability",
                        "as": "row",
                        "in": {
                            "start_date": "$$row.start_date",
                            "end_date": "$$row.end_date",
                            "duration": {
                                "$dateDiff": {
                                    "startDate": "$$row.start_date",
                                    "endDate": "$$row.end_date",
                                    "unit": "day",
                                }
                            },
                            "total_cost": {
                                "$multiply": [
                                    {
                                        "$dateDiff": {
                                            "startDate": "$$row.start_date",
                                            "endDate": "$$row.end_date",
                                            "unit": "day",
                                        }
                                    },
                                    "$cost",
                                ]
                            },
                        },
                    }
                }
            }
        },
        {
            "$match": {
                "availability": {"$elemMatch": {"total_cost": {"$lte": budget}}},
                "skills": {"$all": skills},
            }
        },
    ]
    if reviews__gte:
        aggr_pipeline[1]["$match"]["reviews"] = ({"$gte": reviews__gte},)

    providers = await ServiceProviderModel.aggregate(
        aggregation_pipeline=aggr_pipeline, projection_model=ServiceProviderModel
    ).to_list()
    return providers


@app.get("/populate_mock_data", response_description="Add 3 items into collection")
async def populate_mock_data():
    """Fast impl route to push some data in db"""
    for data in testdata:
        provider = jsonable_encoder(data)
        try:
            new_provider = await ServiceProviderModel(**provider).create()
        except Exception as exc:
            # in case id its already existing
            pass
    return {"OK": "OK"}


@app.on_event("startup")
async def startup_event():
    mongodb_client = AsyncIOMotorClient(MONGO_DB_URL)
    await init_beanie(mongodb_client[MONGO_DB], document_models=[ServiceProviderModel])
    app.include_router(
        ServiceProviderRouter, tags=["ServiceProvider"], prefix="/service_provider"
    )
