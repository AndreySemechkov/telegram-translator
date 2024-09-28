from pydantic import BaseModel
from pydantic_mongo import ObjectIdField
from typing import Optional  # type: ignore


## DB Models


class DBMessage(BaseModel):
    id: ObjectIdField = None
    msgId: int  # PK
    msgOrig: str
    msgEN: str
    msgHE: str
    username: str
    mediaURL: Optional[str]
    date: int


## API Models


class APIBaseResponse(BaseModel):
    statusCode: int
    headers: dict
    body: str


class APIMessage(BaseModel):
    id: int
    title: str
    message: str
    username: str
    has_media: bool
    media_url: str = ""
    english: str
    hebrew: str
    date: int
    link: str = ""

    def __init__(self, **data):
        super().__init__(**data)
        self.link = f"https://t.me/{self.username}/{self.id}"
        self.media_url = (
            f"https://tg.i-c-a.su/media/{self.username}/{self.id}/preview"
            if self.has_media
            else ""
        )


class APIListBody(BaseModel):
    messages: list[APIMessage]
    totalCount: int
