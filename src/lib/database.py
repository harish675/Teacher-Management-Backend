from pymongo import MongoClient, errors
import logging
import sys

from src.config.config import mongo_url, db_name

logging.getLogger("pymongo").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


class MongoDBConnection:
    _instance = None  # Singleton instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(MongoDBConnection, cls).__new__(cls)
        return cls._instance

    def __init__(self, mongo_url: str = None, db_name: str = None):
        if not hasattr(self, "initialized"):  # Ensure __init__ runs only once
            self.mongo_url = mongo_url
            self.db_name = str(db_name) if db_name else None  # Ensure it's a string
            self.client = None
            self._db = None
            self.logger = logging.getLogger(__name__)
            self.initialized = True

    def connect(self):
        if self._db is not None:  # Already connected
            return

        if not self.db_name:
            self.logger.error("Database name is not set. Check your configuration.")
            sys.exit(1)

        try:
            self.client = MongoClient(
                self.mongo_url,
                serverSelectionTimeoutMS=5000,
                socketTimeoutMS=5000,
                connectTimeoutMS=10000,
                maxPoolSize=3,
                retryWrites=False,
            )

            # Attempt to connect and check server status
            self.client.admin.command("ping")
            self.logger.debug(f"Connecting to MongoDB with database: {self.db_name}")
            self._db = self.client[self.db_name]

            self.logger.debug(f"Successfully connected to MongoDB: {self.db_name}")

        except errors.ServerSelectionTimeoutError as err:
            self.logger.error(f"Failed to connect to MongoDB: {err}")
            sys.exit(1)  # Exit the application if connection fails

        if self._db is None:
            self.logger.error("Database connection failed. Shutting down the application.")
            sys.exit(1)

    @property
    def db(self):
        if self._db is None:
            self.connect()  # Ensure the connection is established
        return self._db

    def close(self):
        if self.client is not None:
            self.client.close()
            self.logger.debug("MongoDB connection closed.")


# Usage example
mongo_connection = MongoDBConnection(mongo_url, db_name)