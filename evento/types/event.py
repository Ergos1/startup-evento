from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

from .base_pagination_filter import BasePaginationFilter


class EventListSchema(BasePaginationFilter):
    only_subscribed: bool = Field(default=False, alias="onlySubscribed")


class EventScheduleInSchema(BaseModel):
    start_date: date = Field(alias="startDate")
    end_date: date = Field(alias="endDate")
    description: str


class CreateEventSchema(BaseModel):
    """DTO for event creation"""

    category_ids: list[int] = Field(alias="categoryIds")
    start_date: date = Field(alias="startDate")
    end_date: date = Field(alias="endDate")
    address: str
    description: str

    link_to_registration: Optional[str] = Field(alias="linkToRegistration")
    link_to_buy_ticket: Optional[str] = Field(alias="linkToBuyTicket")

    schedules: list[EventScheduleInSchema]


class EventCategoryOutSchema(BaseModel):
    name: str

    class Config:
        orm_mode = True


class EventScheduleOutSchema(BaseModel):
    start_date: date = Field(alias="startDate")
    end_date: date = Field(alias="endDate")
    description: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class EventOutSchema(BaseModel):
    """DTO to get event"""

    id: int

    start_date: date = Field(alias="startDate")
    end_date: date = Field(alias="endDate")
    address: str
    description: str

    link_to_registration: Optional[str] = Field(alias="linkToRegistration")
    link_to_buy_ticket: Optional[str] = Field(alias="linkToBuyTicket")

    categories: list[EventCategoryOutSchema]
    schedules: list[EventScheduleOutSchema]

    is_subscribed: bool = Field(default=False, alias="isSubscribed")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class SubscribeInSchema(BaseModel):
    """DTO to subscribe user to event"""

    event_id: int = Field(alias="eventId")

    class Config:
        allow_population_by_field_name = True


class SubscribeOutSchema(BaseModel):
    participants_count: int = Field(alias="participantsCount")

    class Config:
        allow_population_by_field_name = True
