from typing import Protocol, Self, NoReturn, Annotated

from fastapi import status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.exceptions import HTTPException

from src.apps.v1.applications.repositories.application_repository import (
    ApplicationSQLARepository,
)
from src.apps.v1.applications.schemas import (
    ApplicationReadSchema,
    ApplicationFilterSchema,
)
from src.core.logger import logger
from src.core.schemas import PaginatedResponseSchema
from src.sqla.db.db_service import db_service


class GetApplicationsFilteredListUseCaseProtocol(Protocol):
    async def get_filtered_list(
        self: Self, data: ApplicationFilterSchema
    ) -> PaginatedResponseSchema[ApplicationReadSchema] | NoReturn: ...


class GetApplicationsFilteredListUseCaseImpl(
    GetApplicationsFilteredListUseCaseProtocol
):
    def __init__(self: Self, session: AsyncSession) -> None:
        self.session = session

    async def get_filtered_list(
        self: Self, data: ApplicationFilterSchema
    ) -> PaginatedResponseSchema[ApplicationReadSchema] | NoReturn:
        try:
            res = await ApplicationSQLARepository(
                session=self.session
            ).filter_by_username(data)
        except Exception as e:
            logger.error(
                "Error while getting Application filtered response from repository: %s",
                str(e),
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Something went wrong while handling request. Please, try again later",
            )
        return res


def get_application_filtered_list(
    session: Annotated[AsyncSession, Depends(db_service.get_async_session)],
) -> GetApplicationsFilteredListUseCaseProtocol:
    return GetApplicationsFilteredListUseCaseImpl(session)
