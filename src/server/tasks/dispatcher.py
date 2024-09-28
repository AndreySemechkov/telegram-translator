from string import Template
from src.server.events import EventType, Events
from src.server.database import Collection, get_db_client


MSGS_BULK_SIZE = 100
URL_TMPLT = Template("https://tg.i-c-a.su/json/$channel?limit=$size")
CHANNELS_EVENT_LIMIT = 100


# lambda handler
def handler(event, context):
    print("Running dispatcher lambda...")
    channels = get_channels()
    events_details = []
    for channel in channels:
        url = URL_TMPLT.substitute({"channel": channel["channelName"], "size": MSGS_BULK_SIZE})
        events_details.append(Events.create_event({"url": url}, EventType.ScraperDispatched))
    print(f"Sending {len(events_details)} events.")
    Events.send_events(events_details)

def get_channels():
    db_client = get_db_client(Collection.Channels.value)
    return db_client.getItems(CHANNELS_EVENT_LIMIT)

    
    
