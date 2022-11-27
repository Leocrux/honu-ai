from typing import Optional
import uuid
from pydantic import BaseModel, Field
from beanie import Document
from datetime import datetime


class ServiceProviderSchema(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str = Field(...)
    skills: list[str] = Field(...)
    cost: int = Field(..., gt=0)
    availability: list[tuple[datetime, datetime]] = Field(...)  # todo need to check a bunch of things here
    reviews: Optional[float] = Field(None, gt=0.0, le=5.0)

    class Config:
        schema_extra = {
            "example": {
                "name": "SEO Inc",
                "skills": ["A skill", "No skill"],
                "cost": 250,
                "availability": [("2022-11-01T00:00", "2022-11-10T00:00"), ("2022-11-20T00:00", "2022-11-22T00:00")],
                "reviews": 3.5,
            }
        }


class ServiceProviderModel(ServiceProviderSchema, Document):
    class Settings:
        name = "service_provider_collection"


class UpdateServiceProviderSchema(BaseModel):
    name: Optional[str]
    skills: Optional[list[str]]
    cost: Optional[float]
    availability: Optional[list[tuple[datetime, datetime]]]
    reviews: Optional[float]
