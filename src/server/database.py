#!/usr/bin/python3
from enum import Enum
import os
from typing import Optional
from pymongo import MongoClient
from pydantic_mongo import AbstractRepository  # type: ignore
from src.server.models import DBMessage
from .creds import MONGO_COLLECTION, MONGO_DB

DB_CLIENT = None

class Collection(str,Enum):
    Content = "content"
    Channels = "channels"
    
class DBCredentials:
    def __init__(self, username, password, host, port, database_name, url=None):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.database_name = database_name
        self.url = url

    @classmethod
    def from_env(cls):
        """
        Initialize MongoDB credentials from environment variables.
        """
        url = os.environ.get("MONGO_DB_URL", "")
        host = os.environ.get("MONGO_HOST", "localhost")
        port = int(os.environ.get("MONGO_PORT", "27017"))
        username = os.environ.get("MONGO_USERNAME")
        password = os.environ.get("MONGO_PASSWORD")
        database_name = os.environ.get("MONGO_DB_NAME")

        if not url and not all([host, port, username, password, database_name]):
            raise Exception("Missing DB credentials")

        return cls(host, port, username, password, database_name, url)

    def get_connection_string(self):
        """
        Construct and return the MongoDB connection string.
        """
        connection_string = (
            self.url
            or f"mongodb+srv://{self.username}:{self.password}@{self.host}:{self.port}/?retryWrites=true&w=majority"
        )
        return connection_string


def get_messages_collection(database, collection_name=Collection.Content.value):
    class MessagesCollection(AbstractRepository[DBMessage]):
        class Meta:
            collection_name = None 
        def __init__(self,database, collection_name):
            self.Meta.collection_name = collection_name
            super().__init__(database)
            
    return MessagesCollection(database, collection_name)



class MongoConn(AbstractRepository[DBMessage]):
    def __init__(self, connstr: str, collection_name: str = None):
        self.client = MongoClient(connstr)
        self.db = self.client[MONGO_DB]
        collection_name = collection_name or MONGO_COLLECTION
        self.collection = get_messages_collection(self.db, collection_name)

    def insert(
        self,
        msgId: int,
        msgOrig: str,
        msgs: dict[str, str],
        username: str,
        mediaURL: str,
        date: int,
    ):
        self.collection.save(
            DBMessage(
                msgId=msgId,
                msgOrig=msgOrig,
                msgs=msgs,
                username=username,
                mediaURL=mediaURL,
                date=date,
            )
        )

    def insertMessage(self, message):
        self.collection.save(message)

    def close(self):
        self.client.close()

    def num(self):
        return self.collection.get_collection().count_documents({})

    def findMsg(self, msgId: int):
        return self.collection.find_one_by({"msgId": msgId})

    def doesExist(self, msgId: int):
        return self.findMsg(msgId) is not None

    def getItems(self, num: int, offset: int = 0, query: str = ""):
        pipeline = []

        if query:
            pipeline.append(self._get_query_match(query))

        pipeline.extend([{"$sort": {"date": -1}}, {"$skip": offset}, {"$limit": num}])

        return self.collection.get_collection().aggregate(pipeline)

    def get_total_items_by_query(self, query: str = ""):
        pipeline = []

        if query:
            pipeline.append(self._get_query_match(query))

        pipeline.extend([{"$count": "totalDocuments"}])

        cursor = self.collection.get_collection().aggregate(pipeline)
        total_count = next(cursor, {"totalDocuments": 0})["totalDocuments"]
        return total_count

    def _get_query_match(self, query: str):
        return {
            "$match": {
                "$or": [
                    {"msgEN": {"$regex": query, "$options": "i"}},
                    {"msgHE": {"$regex": query, "$options": "i"}},
                    {"msgOrig": {"$regex": query, "$options": "i"}},
                ]
            }
        }


def get_db_client(collection_name: Optional[str] = None):
    global DB_CLIENT
    if DB_CLIENT:
        return DB_CLIENT

    db_creds = DBCredentials.from_env() 
    DB_CLIENT = MongoConn(db_creds.get_connection_string(), collection_name)
    return DB_CLIENT
