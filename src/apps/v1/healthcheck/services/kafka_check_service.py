import time
from typing import Annotated, Self, Literal

from fastapi import Depends

from src.apps.v1.healthcheck.schemas import ServiceHealthcheckResponseSchema
from src.apps.v1.healthcheck.services.protocols import BaseHealthCheckServiceProtocol
from src.kafka.kafka_service import AsyncKafkaProducerService, get_kafka_service


class KafkaHealthCheckService(BaseHealthCheckServiceProtocol):
    def __init__(
        self: Self,
        kafka_service: Annotated[AsyncKafkaProducerService, Depends(get_kafka_service)],
    ) -> None:
        self.kafka_service = kafka_service

    async def execute(self: Self) -> ServiceHealthcheckResponseSchema:
        error_message: str | None = None
        start: float = time.perf_counter()
        status: Literal["OK", "ERROR"] = "OK"
        try:
            assert (await self.kafka_service.healthcheck()) is True
        except Exception as e:
            status = "ERROR"
            error_message = str(e)
        finally:
            elapsed_time: float = round(time.perf_counter() - start, 5)

        return ServiceHealthcheckResponseSchema(
            name="kafka",
            status=status,
            response_time=elapsed_time,
            error_message=error_message,
        )
