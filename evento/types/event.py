from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class EventScheduleInSchema(BaseModel):
    start_date: date
    end_date: date
    description: str


class CreateEventSchema(BaseModel):
    """DTO for event creation"""

    category_ids: list[int]
    start_date: str
    end_date: str
    address: str
    description: str

    link_to_registration: Optional[str]
    link_to_buy_ticket: Optional[str]

    schedules: list[EventScheduleInSchema]


class EventCategoryOutSchema(BaseModel):
    name: str

    class Config:
        orm_mode = True


class EventScheduleOutSchema(BaseModel):
    start_date: date
    end_date: date
    description: str

    class Config:
        orm_mode = True


class EventOutSchema(BaseModel):
    """DTO to get event"""

    id: int

    start_date: date
    end_date: date
    address: str
    description: str

    link_to_registration: Optional[str]
    link_to_buy_ticket: Optional[str]

    categories: list[EventCategoryOutSchema]
    schedules: list[EventScheduleOutSchema]

    class Config:
        orm_mode = True


class SubscribeSchema(BaseModel):
    """DTO to subscribe user to event"""

    event_id: int
