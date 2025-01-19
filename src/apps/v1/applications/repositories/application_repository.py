from typing import Self, NoReturn

import sqlalchemy as sa

from src.apps.v1.applications.models import Application
from src.apps.v1.applications.schemas import (
    ApplicationReadSchema,
    ApplicationCreateSchema,
    ApplicationUpdateSchema,
    ApplicationFilterSchema,
)
from src.core.schemas import PaginatedResponseSchema
from src.sqla.pagination import SQLAlchemyModelPaginator
from src.sqla.base_repository import BaseSQLAlchemyRepositoryImpl


class ApplicationPagination(SQLAlchemyModelPaginator[ApplicationReadSchema]):
    pagination_item_type = ApplicationReadSchema


class ApplicationSQLARepository(
    BaseSQLAlchemyRepositoryImpl[
        Application,
        ApplicationReadSchema,
        ApplicationCreateSchema,
        ApplicationUpdateSchema,
    ]
):
    model_type = Application
    read_schema_type = ApplicationReadSchema
    paginator_class = ApplicationPagination

    async def filter_by_username(
        self: Self, filter_schema: ApplicationFilterSchema
    ) -> PaginatedResponseSchema[ApplicationReadSchema] | NoReturn:
        try:
            stmt = sa.select(self.model_type)
            if filter_schema.user_name:
                stmt = stmt.filter(self.model_type.user_name == filter_schema.user_name)

            model_paginator = self.paginator_class(self.session)

            return await model_paginator.get_list(
                statement=stmt,
                page=filter_schema.page,
                page_size=filter_schema.page_size,
            )
        except Exception as e:
            self.handle_errors(e)
