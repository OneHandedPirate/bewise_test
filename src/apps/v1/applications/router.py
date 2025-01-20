from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from src.apps.v1.applications.schemas import (
    ApplicationReadSchema,
    ApplicationCreateSchema,
    ApplicationFilterSchema,
)
from src.apps.v1.applications.use_cases.create_application import (
    CreateApplicationUseCaseProtocol,
    get_create_application_user_case,
)
from src.apps.v1.applications.use_cases.get_filtered_list import (
    GetApplicationsFilteredListUseCaseProtocol,
    get_application_filtered_list,
)
from src.core.schemas import PaginatedResponseSchema


router: APIRouter = APIRouter(prefix="/applications", tags=["applications"])


@router.post(
    "", response_model=ApplicationReadSchema, status_code=status.HTTP_201_CREATED
)
async def create_application(
    data: ApplicationCreateSchema,
    create_application_use_case: Annotated[
        CreateApplicationUseCaseProtocol, Depends(get_create_application_user_case)
    ],
) -> ApplicationReadSchema:
    """Create new Application"""
    return await create_application_use_case.create(data)


@router.get("/filter", response_model=PaginatedResponseSchema[ApplicationReadSchema])
async def filter_by_user_name(
    application_filtered_list_use_case: Annotated[
        GetApplicationsFilteredListUseCaseProtocol,
        Depends(get_application_filtered_list),
    ],
    page: int = Query(default=1, gt=0),
    page_size: int = Query(default=20, gt=0),
    user_name: str = Query(default=None),
) -> PaginatedResponseSchema[ApplicationReadSchema]:
    """
    Paginated Applications list,
    user_name query parameter is optional and case-sensitive
    """
    filter_schema = ApplicationFilterSchema(
        page_size=page_size, page=page, user_name=user_name
    )
    return await application_filtered_list_use_case.get_filtered_list(filter_schema)
