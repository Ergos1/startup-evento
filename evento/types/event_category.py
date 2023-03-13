from pydantic import BaseModel


class EventCategoryListSchema(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True