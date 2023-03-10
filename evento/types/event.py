from datetime import date
from enum import Enum
from typing import Optional 

from pydantic import BaseModel

class Category(str, Enum):
    """Event categories"""

    CINEMA = "CINEMA"
    DEVELOPMENT = "DEVELOPMENT"
    ENTARTAINMENT = "ENTARTAINMENT"
    CONCERT = "CONCERT"
    SPORT = "SPORT"
    ART = "ART"
    WORLD_EVENT = "WORLD_EVENT"
    WORKSHOP = "WORKSHOP"
    TOUR = "TOUR"
    TRIP = "TRIP"


class EventScheduleInSchema(BaseModel):
    start_date: date
    end_date: date
    description: str


class EveneCategoryInSchema(BaseModel):
    id: int


class CreateEventSchema(BaseModel):
    """DTO for event creation"""

    categories: list[EveneCategoryInSchema]
    start_date: str
    end_date: str
    address: str
    description: str

    link_to_registration: Optional[str]
    link_to_buy_ticket: Optional[str]

    schedules: list[EventScheduleInSchema]


class EventCategoryOutSchema(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class EventScheduleOutSchema(BaseModel):
    id: int
    start_date: date
    end_date: date
    description: str

    class Config:
        orm_mode = True


class GetEventOutSchema(BaseModel):
    """DTO to get event"""

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