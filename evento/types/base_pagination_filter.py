from fastapi import Query
from pydantic import BaseModel, Field


class BasePaginationFilter(BaseModel):
    page: int = Query(1, ge=1)
    limit: int = Query(10, ge=1, le=100)
    search_text: str = Field("", alias="searchText")

    def offset(self):
        return (self.page - 1) * self.limit
