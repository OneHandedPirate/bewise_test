from typing import TypeVar, Self

from aiokafka import AIOKafkaProducer
from pydantic import BaseModel

from src.core.config import settings


MessageData = TypeVar("MessageData", bound=BaseModel)


class AsyncKafkaProducerService:
    def __init__(self: Self, bootstrap_servers: str) -> None:
        self.bootstrap_servers = bootstrap_servers
        self.producer: AIOKafkaProducer | None = None

    async def start(self: Self) -> None:
        self.producer = AIOKafkaProducer(bootstrap_servers=self.bootstrap_servers)
        await self.producer.start()

    async def stop(self: Self) -> None:
        if self.producer:
            await self.producer.stop()

    async def send_message(self: Self, topic: str, message: MessageData) -> None:
        if not self.producer:
            raise RuntimeError("Kafka Producer is not started. Call start() first.")

        serialized_message = message.model_dump_json()
        await self.producer.send_and_wait(topic, serialized_message.encode("utf-8"))

    async def healthcheck(self: Self) -> bool:
        if not self.producer:
            raise RuntimeError("Kafka Producer is not started. Call start() first.")
        await self.producer.client.bootstrap()
        return True


kafka_service: AsyncKafkaProducerService = AsyncKafkaProducerService(
    f"{settings.kafka.host}:{settings.kafka.port}"
)


async def get_kafka_service() -> AsyncKafkaProducerService:
    if not kafka_service.producer:
        await kafka_service.start()
    return kafka_service
