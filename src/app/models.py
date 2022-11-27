from typing import Optional
import uuid
from pydantic import BaseModel, Field, validator
from beanie import Document
from datetime import date, datetime
from typing_extensions import TypedDict


class DateRange(TypedDict):
    start_date: date
    end_date: date


class ServiceProviderSchema(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str = Field(...)
    skills: list[str] = Field(...)
    cost: int = Field(..., gt=0)
    availability: list[DateRange] = Field(...)
    reviews: Optional[float] = Field(None, gt=0.0, le=5.0)

    @validator("availability")
    def start_date_prior_end_date(cls, availability):
        for v in availability:
            if v["start_date"] >= v["end_date"]:
                raise ValueError(f"Availability {v} start date after end date")
        return availability

    class Config:
        schema_extra = {
            "example": {
                "name": "SEO Inc",
                "skills": ["A skill", "No skill"],
                "cost": 250,
                "availability": [
                    {"start_date": "2022-11-01", "end_date": "2022-11-10"},
                    {"start_date": "2022-12-01", "end_date": "2022-12-10"},
                ],
                "reviews": 3.5,
            }
        }


class ServiceProviderModel(ServiceProviderSchema, Document):
    class Settings:
        name = "service_provider_collection"
        bson_encoders = {date: lambda o: datetime.combine(o, datetime.min.time())}


class UpdateServiceProviderSchema(BaseModel):
    name: Optional[str]
    skills: Optional[list[str]]
    cost: Optional[float]
    availability: Optional[list[DateRange]]
    reviews: Optional[float]

    @validator("availability")
    def start_date_prior_end_date(cls, availability):
        for v in availability:
            if v["start_date"] >= v["end_date"]:
                raise ValueError(f"Availability {v} start date after end date")
        return availability

    class Config:
        schema_extra = {
            "example": {
                "name": "SEO Inc",
                "skills": ["A skill", "No skill"],
                "cost": 250,
                "availability": [
                    {"start_date": "2022-11-01", "end_date": "2022-11-10"},
                    {"start_date": "2022-12-01", "end_date": "2022-12-10"},
                ],
                "reviews": 3.5,
            }
        }
