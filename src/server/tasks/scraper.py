#!/usr/bin/python3

import asyncio
import json
from pydantic import BaseModel

from src.server.events import EventBridgeEvent
from ..database import get_db_client
import src.server.tasks.scraper_utils as scraper_utils
from src.server.tasks.media_handler import MediaHandler

# lambda handler
def fetch(event, context):
    print(f"Running message scraper lambda with event {event}...")
    parsed_event = EventBridgeEvent.parse_event(event)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(scrape_feed(parsed_event))


def get_media_url(message, msg_data, username):
    media_url = MediaHandler(message, username).store()
    if media_url:
        return media_url

    print(f"Failed to store media for message {msg_data.msgId}")
    if "media" in message:
        return f"https://tg.i-c-a.su/media/{username}/{msg_data.msgId}/preview"

    print(f"Message {msg_data.msgId} has no media")
    return None


async def scrape_feed(scrape_event):

    feed_url = scrape_event.detail.get("url")
    if not feed_url:
        print("Got an event with empty url, exiting")
        return []
    
    db_client = get_db_client()
    translate_service = scraper_utils.get_google_translate_service()

    # Create an instance of the html2text converter
    html_converter = scraper_utils.get_html_converter()

    json_data = scraper_utils.fetch_raw_data(feed_url)
    messages = json_data.get("messages", [])
    if not messages:
        print("This bulk has no messages!")
        return

    print(f"Recieved {len(messages)} messages.")

    msgs_persisted = []
    for message in messages:
        username = json_data["chats"][0]["username"]
        msg_data = await scraper_utils.get_message_data(
            message, username, html_converter, translate_service
        )
        if not msg_data:
            continue

        if db_client.doesExist(msg_data.msgId):
            print(f"Message {msg_data.msgId} already exists. Skipping...")
            continue

        msg_data.mediaURL = get_media_url(message, msg_data, username)

        scraper_utils.persist_msg_data(db_client, msg_data)
        msgs_persisted.append(msg_data)

    print(f"Persisted {len(msgs_persisted)} of {len(messages)} messages.")
    return msgs_persisted
