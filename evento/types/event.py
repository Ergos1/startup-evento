from enum import Enum


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
