from enum import Enum
import os
import typing
import requests
import html2text
from googleapiclient.discovery import build
from ..database import DBMessage


class Language(str, Enum):
    HE = "he"
    EN = "en"
    AR = "ar"


def get_google_translate_service():
    translation_developer_key = os.environ["GOOGLE_TRANSLATE_API"]
    # Init Google Translate API client. Check init to reuse connection.
    return build("translate", "v2", developerKey=translation_developer_key)


def get_html_converter():
    # Create an instance of the html2text converter
    html_converter = html2text.HTML2Text()
    html_converter.ignore_links = True  # Ignore links in the HTML content
    return html_converter


def fetch_raw_data(url):
    print(f"Receiving data from {url}...")
    response = requests.get(url)
    return response.json()


async def translate(translate_service, src: str, target: str, data: str):
    return (
        translate_service.translations()
        .list(source=src, target=target, q=[data])
        .execute()
    )


async def get_message_data(
    message,
    username: str,
    html_converter: html2text.HTML2Text,
    translate_service: typing.Any,
):
    raw_description = message.get("message", "")
    if raw_description is None:
        print("Message description is None. Skipping the msg.")
        return None

    raw_description = raw_description.strip()  # Get and clean the message text
    if not len(raw_description):
        print("Message description is not set. Skipping the msg.")
        return None

    message_id = message.get("id", "")  # Assuming you have a message ID
    if not message_id:
        print("Message id is missing. Skipping the msg.")
        return None

    date = message.get("date", 0)

    # Convert HTML to plain text and clean the description
    description = html_converter.handle(raw_description)

    media_url = (
        f"https://tg.i-c-a.su/media/{username}/{message_id}/preview"
        if "media" in message
        else None
    )

    async def getTranslation(language):
        translation_result = await translate(
            translate_service, Language.AR.value, language, description
        )
        return translation_result["translations"][0]["translatedText"]

    msgs: dict[str, str] = {}
    msgs[Language.EN.value] = await getTranslation(Language.EN.value)
    msgs[Language.HE.value] = await getTranslation(Language.HE.value)

    return DBMessage(
        msgId=message_id,
        msgOrig=description,
        msgEN=msgs[Language.EN.value],
        msgHE=msgs[Language.HE.value],
        username=username,
        mediaURL=media_url,
        date=date,
    )


def persist_msg_data(db_client, msg_data):
    db_client.insertMessage(msg_data)
    