from enum import Enum
import json
from typing import List
import boto3

EVENT_SRC = "ironwatcher.app"
EVENT_BUS = "ironwatcherBus"

class EventType(str, Enum):
    ScraperDispatched = "ScraperDispatched"

class Events:
    @staticmethod
    def create_event(details: dict, type: EventType, src: str = EVENT_SRC, bus: str = EVENT_BUS):
        return {
                    'Source': src,
                    'DetailType': type.value,
                    'Detail': json.dumps(details),
                    'EventBusName': bus
                }
    
    @staticmethod
    def send_events(events: List[str]):
        response = boto3.client('events', ).put_events(
            Entries=events
        )

        # Handle the response (optional)
        if response['FailedEntryCount']:
            raise Exception(f"Failed to send {response['FailedEntryCount']} events")

class EventBridgeEvent:
    def __init__(self, source, type, detail):
        self.source = source
        self.type = type
        self.detail = detail

    @classmethod
    def parse_event(cls, event):
        # Extract relevant information from the EventBridge event
        event_source = event.get("source", "Unknown Source")
        detail_type = event.get("detail-type", "Unknown Detail Type")
        event_detail = event.get("detail", {})

        return cls(event_source, detail_type, event_detail)




