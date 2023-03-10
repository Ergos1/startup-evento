
from pydantic import BaseModel


class BasePaginationFilter(BaseModel):
    page: int
    size: int
    sort: str
    order: str

    def offset(self):
        return self.page * self.size