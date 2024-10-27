from typing import Any, Dict, List, Optional
from uagents import Agent, Context, Model, Bureau
from uagents.setup import fund_agent_if_low
from uagents import Model

class Coordinates(Model):
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

AGENT_MAILBOX_KEY = "3d183117-a137-486e-896a-1ae3bc4f6ff3"
agent = Agent(name="user",
    seed = 'my final attempt',
    mailbox=f"{AGENT_MAILBOX_KEY}@https://agentverse.ai",
    port = 8001)

GMAPS_AGENT_ADDRESS = "agent1qt2ugt8egv72es0fq2md2sj5waxz0k347pgakfsx706pfpq8z9n759p9k4g"

example_request = POIAreaRequest(
    loc_search=Coordinates(latitude=48.140505822096365, longitude=11.559987118245475),
    radius_in_m=500,
    query_string="coffee shop",
)


@agent.on_event("startup")
async def handle_startup(ctx: Context):
    await ctx.send(GMAPS_AGENT_ADDRESS, example_request)
    ctx.logger.info(f"Sent request to  agent: {example_request}")


@agent.on_message(POIResponse)
async def handle_response(ctx: Context, sender: str, msg: POIResponse):
    ctx.logger.info(f"Received {len(msg.data)} pois from: {sender}")
    for place in msg.data:
        ctx.logger.info(place.location_name)


if __name__ == "__main__":
    agent.run()
