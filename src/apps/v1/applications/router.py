from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import PositiveInt

from src.apps.v1.applications.repositories.application_repository import (
    ApplicationSQLARepository,
)
from src.apps.v1.applications.schemas import (
    ApplicationReadSchema,
    ApplicationCreateSchema,
    ApplicationFilterSchema,
)
from src.core.schemas import PaginatedResponseSchema
from src.sqla.db.db_service import db_service


router: APIRouter = APIRouter(prefix="/applications", tags=["applications"])


@router.post("", response_model=ApplicationReadSchema)
async def create_application(
    data: ApplicationCreateSchema,
    session: Annotated[AsyncSession, Depends(db_service.get_async_session)],
) -> ApplicationReadSchema:
    """Create new Application"""
    return await ApplicationSQLARepository(session=session).create(data)


@router.get(
    "/filter",
    response_model=PaginatedResponseSchema[ApplicationReadSchema]
)
async def filter_by_user_name(
    session: Annotated[AsyncSession, Depends(db_service.get_async_session)],
    page: PositiveInt = Query(default=1),
    page_size: PositiveInt = Query(default=20),
    user_name: str = Query(default=None),
) -> PaginatedResponseSchema[ApplicationReadSchema]:
    """
    Paginated Applications list,
    user_name filter is optional and case-sensitive
    """
    filter_schema = ApplicationFilterSchema(
        page_size=page_size,
        page=page,
        user_name=user_name
    )

    return await ApplicationSQLARepository(session=session).filter_by_username(
        filter_schema
    )
