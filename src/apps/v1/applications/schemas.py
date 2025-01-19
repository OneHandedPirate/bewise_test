from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from src.core.schemas import PaginationSchema, UpdateBaseModel


class ApplicationReadSchema(BaseModel):
    id: UUID
    user_name: str = Field(max_length=60)
    description: str


class ApplicationCreateSchema(BaseModel):
    user_name: str = Field(max_length=60)
    description: str


class ApplicationUpdateSchema(UpdateBaseModel):
    user_name: Optional[str] = Field(max_length=60, default=None)
    description: Optional[str] = None


class ApplicationFilterSchema(PaginationSchema):
    user_name: Optional[str] = None
