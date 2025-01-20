from typing import Protocol, Self, NoReturn, Annotated

from fastapi import status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.exceptions import HTTPException

from src.apps.v1.applications.repositories.application_repository import (
    ApplicationSQLARepository,
)
from src.apps.v1.applications.schemas import (
    ApplicationCreateSchema,
    ApplicationReadSchema,
)
from src.core.config import settings
from src.core.logger import logger
from src.kafka.kafka_service import AsyncKafkaProducerService, get_kafka_service
from src.sqla.db.db_service import db_service


class CreateApplicationUseCaseProtocol(Protocol):
    async def create(
        self: Self, data: ApplicationCreateSchema
    ) -> ApplicationReadSchema | NoReturn: ...


class CreateApplicationUseCaseImpl(CreateApplicationUseCaseProtocol):
    def __init__(
        self: Self, session: AsyncSession, kafka: AsyncKafkaProducerService
    ) -> None:
        self.session = session
        self.kafka = kafka

    async def create(
        self: Self, data: ApplicationCreateSchema
    ) -> ApplicationReadSchema | NoReturn:
        try:
            res: ApplicationReadSchema = await ApplicationSQLARepository(
                session=self.session
            ).create(data)
        except Exception as e:
            logger.error("Error occurred while creating new application: %s", str(e))
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Something went wrong while creating new application",
            )
        logger.info(
            "New application created and saved to db. Application id: %s", str(res.id)
        )

        try:
            await self.kafka.send_message(topic=settings.kafka.topic_name, message=res)
        except Exception as e:
            logger.error(
                "Error occurred while publishing Application data for id: %s. Error: %s",
                str(res.id),
                str(e),
            )
        logger.info("Application data %s successfully published to kafka", str(res.id))

        return res


def get_create_application_user_case(
    session: Annotated[AsyncSession, Depends(db_service.get_async_session)],
    kafka: Annotated[AsyncKafkaProducerService, Depends(get_kafka_service)],
) -> CreateApplicationUseCaseProtocol:
    return CreateApplicationUseCaseImpl(session, kafka)
