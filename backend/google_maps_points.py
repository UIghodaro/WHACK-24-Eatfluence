from typing import Any, Dict, List, Optional

from uagents import Model, Context, Agent
from uagents.setup import fund_agent_if_low
import trend_scraper

class Coordinates(Model):
    latitude: float
    longitude: float

class GeolocationResponse(Model):
    latitude: float
    longitude: float


class POIAreaRequest(Model):
    loc_search: Coordinates
    radius_in_m: int
    limit: int = 20
    query_string: str
    filter: Dict[str, Any] = {}


class POI(Model):
    placekey: str
    location_name: str
    brands: Optional[List[str]] = None
    top_category: Optional[str] = None
    sub_category: Optional[str] = None
    location: Coordinates
    address: str
    city: str
    region: Optional[str] = None
    postal_code: str
    iso_country_code: str
    metadata: Optional[Dict[str, Any]] = None


class POIResponse(Model):
    loc_search: Coordinates
    radius_in_m: int
    data_origin: str
    data: List[POI]


from uagents import Agent, Context

AGENT_MAILBOX_KEY = "28ef9025-0b27-45a4-94b4-7d3e44e200bc"

agent = Agent(
    name="user",
    seed = 'user for luis whack 2024',
    mailbox=f"{AGENT_MAILBOX_KEY}@https://agentverse.ai",
)

GMAPS_AGENT_ADDRESS = "agent1qvcqsyxsq7fpy9z2r0quvng5xnhhwn3vy7tmn5v0zwr4nlm7hcqrckcny9e"

@agent.on_message(model = GeolocationResponse)
async def message_handler(ctx: Context, sender : str, msg: GeolocationResponse):
    # ctx.logger.info(f'Recieved message from {sender} : {msg.latitude} , {msg.longitude}')

    await ctx.send(GMAPS_AGENT_ADDRESS, POIAreaRequest(
        loc_search=Coordinates(latitude=msg.latitude, longitude=msg.longitude),
        radius_in_m=500,
        limit=4,
        query_string="restaurant",
    ))

@agent.on_message(POIResponse)
async def handle_response(ctx: Context, sender: str, msg: POIResponse):
    # ctx.logger.info(f"Received {len(msg.data)} pois from: {sender}")

    nearby_places = []

    for place in msg.data:
        ctx.logger.info(place.location_name)
        nearby_places.append(place.location_name)
    
    for n in nearby_places:
        print("Scraping " + str(n))
        trend_scraper.tiktok_scrape(n)

if __name__ == "__main__":
    agent.run()