import pymongo
from pymongo import MongoClient

from src._constants import KEY_SENDER_ID
from src._schemas import Message
from src._settings import settings


class BaseTrackerStore:
    async def get_messages(
        self,
        sender_id: str = None,
        limit: int = 100,
        skip: int = 0,
    ) -> list[Message]:
        raise NotImplementedError("Subclasses must implement this")

    async def insert_message(self, message: Message) -> None:
        raise NotImplementedError("Subclasses must implement this")


class MongoTrackerStore(BaseTrackerStore):
    """
    Implementation of `BaseTrackerStore` that stores conversation history in a MongoDB database.
    """

    def __init__(
        self,
        host: str = None,
        port: int = None,
        username: str = None,
        password: str = None,
    ):
        self.client = MongoClient(
            host=host or settings.MONGODB_HOST,
            port=port or settings.MONGODB_PORT,
            username=username or settings.MONGODB_USER,
            password=password or settings.MONGODB_PASSWORD,
        )
        self.db = self.client[settings.MONGODB_NAME]
        self.trackers_data_collection = self.db["trackers_data"]
        self.trackers_data_collection.create_index([(KEY_SENDER_ID, pymongo.DESCENDING)])

    async def get_messages(
        self,
        sender_id: str = None,
        limit: int = 100,
        skip: int = 0,
    ) -> list[Message]:
        query = {
            KEY_SENDER_ID: sender_id,
        }
        cursor = self.trackers_data_collection.find(query).sort("_id", pymongo.DESCENDING).skip(skip).limit(limit)
        return [Message(**x) for x in cursor]

    async def insert_message(self, message: Message) -> None:
        self.trackers_data_collection.insert_one(message.dict())
