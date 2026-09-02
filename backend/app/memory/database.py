"""MongoDB connection factory, kept lazy so the application can start offline."""

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.config import Settings


class MongoDatabase:
    """Owns the Mongo client used by future persistent memory repositories."""

    def __init__(self, settings: Settings) -> None:
        self._client = AsyncIOMotorClient(settings.mongodb_uri, serverSelectionTimeoutMS=3_000)
        self._database = self._client[settings.mongodb_database]

    @property
    def database(self) -> AsyncIOMotorDatabase:
        return self._database

    async def ping(self) -> bool:
        await self._database.command("ping")
        return True

    def close(self) -> None:
        self._client.close()
