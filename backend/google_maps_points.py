from typing import Any, Dict, List, Optional

from uagents import Model, Context, Agent
from uagents.setup import fund_agent_if_low

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

example_request = POIAreaRequest(
    loc_search=Coordinates(latitude=48.140505822096365, longitude=11.559987118245475),
    radius_in_m=500,
    limit=8,
    query_string="coffee shop",
)


# @agent.on_event("startup")
# async def handle_startup(ctx: Context):
#     ctx.logger.info(agent.address)
#     await ctx.send(GMAPS_AGENT_ADDRESS, example_request)
#     ctx.logger.info(f"Sent request to  agent: {example_request}")


@agent.on_message(model = GeolocationResponse)
async def message_handler(ctx: Context, sender : str, msg: GeolocationResponse):
    ctx.logger.info(f'Recieved message from {sender} : {msg.latitude} , {msg.longitude}')

    await ctx.send(GMAPS_AGENT_ADDRESS, POIAreaRequest(
        loc_search=Coordinates(latitude=msg.latitude, longitude=msg.longitude),
        radius_in_m=500,
        limit=8,
        query_string="coffee shop",
    ))

@agent.on_message(POIResponse)
async def handle_response(ctx: Context, sender: str, msg: POIResponse):
    ctx.logger.info(f"Received {len(msg.data)} pois from: {sender}")
    for place in msg.data:
        ctx.logger.info(place.location_name)
