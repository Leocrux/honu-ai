from fastapi import APIRouter, Request, Body, status, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.models import ServiceProviderSchema, UpdateServiceProvider

router = APIRouter()


@router.get("/", response_description="List all Service Providers")
async def get_providers(request: Request):
    providers = []
    async for provider in request.app.mongodb["service_provider_collection"].find():
        providers.append(provider)
    return providers


@router.post("/", response_description="Add new Service Provider")
async def create_provider(request: Request, provider: ServiceProviderSchema = Body(...)):
    provider = jsonable_encoder(provider)
    new_provider = await request.app.mongodb["service_provider_collection"].insert_one(provider)
    created_provider = await request.app.mongodb["service_provider_collection"].find_one(
        {"_id": new_provider.inserted_id}
    )
    return JSONResponse(status_code=status.HTTP_200_OK, content=created_provider)


@router.get("/{id}", response_description="Get a single provider")
async def show_provider(id: str, request: Request):
    if (provider := await request.app.mongodb["service_provider_collection"].find_one({"_id": id})) is not None:
        return provider
    raise HTTPException(status_code=404, detail=f"Provider {id} not found")


@router.put("/{id}", response_description="Update a provider")
async def update_provider(id: str, request: Request, provider: UpdateServiceProvider = Body(...)):
    provider = {k: v for k, v in provider.dict().items() if v is not None}

    if len(provider) >= 1:
        update_result = await request.app.mongodb["service_provider_collection"].update_one(
            {"_id": id}, {"$set": provider}
        )

        if update_result.modified_count == 1:
            if (
                    updated_provider := await request.app.mongodb["service_provider_collection"].find_one({"_id": id})
            ) is not None:
                return updated_provider

    if (
            existing_provider := await request.app.mongodb["service_provider_collection"].find_one({"_id": id})
    ) is not None:
        return existing_provider

    raise HTTPException(status_code=404, detail=f"provider {id} not found")


@router.delete("/{id}", response_description="Delete provider")
async def delete_provider(id: str, request: Request):
    delete_result = await request.app.mongodb["service_provider_collection"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)

    raise HTTPException(status_code=404, detail=f"Task {id} not found")
