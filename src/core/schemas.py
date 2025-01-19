from typing import TypeVar, Generic
from uuid import UUID

from pydantic import BaseModel, PositiveInt


PaginationItem = TypeVar("PaginationItem", bound=BaseModel)


class UpdateBaseModel(BaseModel):
    id: UUID


class PaginationSchema(BaseModel):
    page: PositiveInt = 1
    page_size: PositiveInt = 20


class PaginatedResponseSchema(PaginationSchema, Generic[PaginationItem]):
    total_pages: int
    total_items: int
    items: list[PaginationItem]
