from typing import Union

from beanie.operators import And, In, Set
from fastapi import APIRouter, Body, HTTPException, Query, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.models import (ServiceProviderModel, ServiceProviderSchema,
                        UpdateServiceProviderSchema)

router = APIRouter()


# CRUD for ServiceProvider


@router.get(
    "/",
    response_description="List all Service Providers",
    response_model=list[ServiceProviderModel],
)
async def get_providers(
    name: Union[str, None] = Query(default=None),
    skills: Union[list[str], None] = Query(default=None),
    cost__gte: Union[int, None] = Query(default=None),
    cost__lt: Union[int, None] = Query(default=None),
    reviews__gte: Union[float, None] = Query(default=None),
    reviews__lt: Union[float, None] = Query(default=None),
):
    query = []
    if skills:
        query.append(In(ServiceProviderModel.skills, skills))
    if name:
        query.append(ServiceProviderModel.name == name)
    if cost__gte:
        query.append(ServiceProviderModel.cost >= cost__gte)
    if cost__lt:
        query.append(ServiceProviderModel.cost < cost__lt)
    if reviews__gte:
        query.append(ServiceProviderModel.reviews >= reviews__gte)
    if reviews__lt:
        query.append(ServiceProviderModel.reviews < reviews__lt)

    providers = await ServiceProviderModel.find(And(*query) if query else {}).to_list()
    return providers


@router.post(
    "/",
    response_description="Add new Service Provider",
    response_model=ServiceProviderSchema,
)
async def create_provider(provider: ServiceProviderSchema = Body(...)):
    provider = jsonable_encoder(provider)
    new_provider = await ServiceProviderModel(**provider).create()
    return new_provider


@router.get(
    "/{id}",
    response_description="Get a single provider",
    response_model=ServiceProviderSchema,
)
async def show_provider(id: str):
    if (
        provider := await ServiceProviderModel.find_one(ServiceProviderModel.id == id)
    ) is not None:
        return provider
    raise HTTPException(status_code=404, detail=f"Provider {id} not found")


@router.put("/{id}", response_description="Update a provider")
async def update_provider(id: str, provider: UpdateServiceProviderSchema = Body(...)):
    provider = {k: v for k, v in provider.dict().items() if v is not None}

    if len(provider) >= 1:
        update_result = await ServiceProviderModel.find_one(
            ServiceProviderModel.id == id
        ).update(Set(provider))

        if update_result.modified_count == 1:
            if (
                updated_provider := await ServiceProviderModel.find_one(
                    ServiceProviderModel.id == id
                )
            ) is not None:
                return updated_provider

    if (
        existing_provider := await ServiceProviderModel.find_one(
            ServiceProviderModel.id == id
        )
    ) is not None:
        return existing_provider

    raise HTTPException(status_code=404, detail=f"provider {id} not found")


@router.delete("/{id}", response_description="Delete provider")
async def delete_provider(id: str):
    delete_result = await ServiceProviderModel.find_one(
        ServiceProviderModel.id == id
    ).delete()

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)

    raise HTTPException(status_code=404, detail=f"Task {id} not found")
