import json
from html import unescape
from loguru import logger
from typing import Optional
from src.server.database import get_db_client
from src.server.models import APIBaseResponse, APIListBody, APIMessage


def get_data(limit: int = 20, page: int = 0, query: str = ""):
    db_client = get_db_client()
    return {
        "documents": db_client.getItems(limit, limit * page, query),
        "totalDocuments": db_client.get_total_items_by_query(query),
    }


def create_message_object(message: dict) -> APIMessage:
    return APIMessage(
        id=message["msgId"],
        title=message["msgOrig"],  # Do we have a title?
        message=message["msgOrig"],
        username=message["username"],
        has_media=True if "mediaURL" in message and message["mediaURL"] else False,
        english=unescape(message["msgEN"]),
        hebrew=unescape(message["msgHE"]),
        date=message["date"],
    )


def get_headers(headers: Optional[dict] = None):
    cors_headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE",
    }

    if headers:
        cors_headers.update(headers)

    return cors_headers


def get_response(
    status_code: int, body: str, headers: Optional[dict] = None
) -> APIBaseResponse:
    return APIBaseResponse(
        statusCode=status_code,
        headers=get_headers(headers),
        body=body,
    )


def get_list(event, context):
    try:
        query_params = event.get("queryStringParameters", {})
        limit = int(query_params.get("limit", 20))
        page = int(query_params.get("page", 1)) - 1
        query = str(query_params.get("query", ""))

        data = get_data(limit, page, query)

        messages = []
        for message in data["documents"]:
            messages.append(create_message_object(message).dict())

        messages_count = len(messages)
        logger.info(f"Returning {messages_count} messages")

        body = APIListBody(
            messages=messages,
            totalCount=data["totalDocuments"],
        )

        return get_response(
            200,
            json.dumps(body.dict()),
        ).dict()

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return get_response(500, json.dumps({"message": "Something went wrong"})).dict()
